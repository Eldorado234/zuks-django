from git import * 
from github import Github
from core.models import FAQ
import glob, os
from markdown import Markdown
from django.conf import settings

# TODO: Handle git errors
class FAQManagement:
	def update_faq():
		# Update FAQ repository
		faq_repo = Repo('content/faq')
		faq_repo.remote().pull()

		# Reset consistency status of all FAQ questions.
		# If no question exists for an question entry, the question will 
		# remain inconsistent and is not shown in the FAQ. 
		# It could be aded later again, the author information will remain.
		for question in FAQ.objects.all():
			question.consistent = False
			question.save()
		
		source_files = glob.glob('content/faq/*.md')
		md = Markdown()
		for source_path in source_files:
			# Get filename without extension (.md)
			file_name = os.path.basename(source_path)[:-3]

			# Check for database consistency
			try:
				question = FAQ.objects.get(slug=file_name)
				question.consistent = True
				question.save()
			except FAQ.DoesNotExist:
				# Question was added directly in the repository
				# Assume, that this question was authored by ZUKS
				FAQ.objects.create( question=file_name,
									slug=file_name,
									author=_("ZUKS"),
									email=_("@zuks-mail"),
									twitter_handle=_("@zuks-twitter"),
									consistent=True)

			# Convert markdown to html files
			target_path = 'templates/core/faq/%s.html' % (file_name,)
			with open(source_path, 'r') as source, open(target_path, 'w') as target:
				html = md.convert(source.read())
				target.write(html)

	def push_question(question):
		# Create a new branch for the question
		localRepo = Repo('content/faq')

		questionBranch = Head.create(localRepo, question.slug)
		questionBranch.checkout()

		# Write the markdown file
		target_path = 'content/faq/%s.md' % (question.slug,)
		with open(target_path, 'w') as target:
			target.write('## %s' % (question.text,))

		# Commit the markdown file
		localRepo.index.add(['%s.md' % (question.slug,)])
		commit_message = 'Added question'
		if question.author:
			commit_message += ' by %s' % (question.author,)
		localRepo.index.commit(commit_message)
		
		# Push new branch
		localRepo.remote().push(questionBranch)

		# Create a pull request for the new branch
		gitHub = Github(settings.GITHUB_TOKEN)

		if settings.GITHUB_ORGANISATION:
			user = gitHub.get_organization(settings.GITHUB_ORGANISATION)
		else:
			user = gitHub.get_organization(settings.GITHUB_USER)
		repo = user.get_repo(settings.GITHUB_REPOSITORY)

		pull_text = 'New question authered'
		if question.author:
			pull_text += ' by %s' % (question.author,)
		if question.twitter_handle:
			pull_text += ' (%s)' % (question.twitter_handle,)
		repo.create_pull(question.text, pull_text, 'master', question.slug)

		# Get back to the master branch
		localRepo.git.checkout('master')