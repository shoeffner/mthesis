proposal:
	pandoc \
		--bibliography=bibliography.bib \
		-o proposal_shoeffner.pdf \
		topicproposal.md

presentation:
	pandoc \
		-t beamer \
		--bibliography=bibliography.bib \
		-o presentation_cvgroup.pdf \
		cvpresentation.md
