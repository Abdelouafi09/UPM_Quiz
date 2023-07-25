// Add option functionality
        var questionSection = document.getElementById('question-section');
        var addQuestionBtn = document.getElementById('add-question');
        var questionCount = 1;

        addQuestionBtn.addEventListener('click', function() {
            questionCount++;
            var newQuestion = document.createElement('div');
            newQuestion.classList.add('question');

            var questionLabel = document.createElement('label');
            questionLabel.textContent = 'Question:';
            var questionInput = document.createElement('input');
            questionInput.type = 'text';
            questionInput.name = 'question[]';
            questionInput.required = true;

            var option1Label = document.createElement('label');
            option1Label.textContent = 'Option 1:';
            var option1Input = document.createElement('input');
            option1Input.type = 'text';
            option1Input.name = 'option-' + questionCount + '[]';
            option1Input.required = true;

            var option2Label = document.createElement('label');
            option2Label.textContent = 'Option 2:';
            var option2Input = document.createElement('input');
            option2Input.type = 'text';
            option2Input.name = 'option-' + questionCount + '[]';
            option2Input.required = true;

            var addOptionBtn = document.createElement('button');
            addOptionBtn.type = 'button';
            addOptionBtn.classList.add('add-option');
            addOptionBtn.textContent = 'Add Option';

            newQuestion.appendChild(questionLabel);
            newQuestion.appendChild(questionInput);
            newQuestion.appendChild(option1Label);
            newQuestion.appendChild(option1Input);
            newQuestion.appendChild(option2Label);
            newQuestion.appendChild(option2Input);
            newQuestion.appendChild(addOptionBtn);

            questionSection.appendChild(newQuestion);
        });

        // Add option functionality
        questionSection.addEventListener('click', function(event) {
            if (event.target.classList.contains('add-option')) {
                var questionDiv = event.target.parentElement;

                var optionCount = questionDiv.querySelectorAll('input[name^="option-"]').length + 1;

                var optionLabel = document.createElement('label');
                optionLabel.textContent = 'Option ' + optionCount + ':';
                var optionInput = document.createElement('input');
                optionInput.type = 'text';
                optionInput.name = 'option-' + questionCount + '[]';
                optionInput.required = true;

                questionDiv.insertBefore(optionLabel, event.target);
                questionDiv.insertBefore(optionInput, event.target);
            }
        });