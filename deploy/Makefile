BRANCH=deploy

check-branch:
	@[ ! -z $(force) ] || [ `git branch --show-current` = ${BRANCH} ] || (echo 'only "${BRANCH}" branch allowed (force=1 to ignore)'; exit 1)

deploy: check-branch
	git stash

	ansible-playbook -i inventory deploy.yml --ask-pass

	git stash pop || true

deploy-test:
	ansible-playbook -i inventory deploy.yml --ask-pass
