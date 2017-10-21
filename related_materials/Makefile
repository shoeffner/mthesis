proposal:
	@mkdir -p ../build
	pandoc \
		--bibliography=../bibliography.bib \
		-o ../build/proposal_shoeffner.pdf \
		topicproposal.md

presentation:
	@mkdir -p ../build
	pandoc \
		-t beamer \
		--bibliography=../bibliography.bib \
		-o ../build/presentation_cvgroup.pdf \
		cvpresentation.md
