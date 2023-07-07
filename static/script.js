// Function to add an option field for a question
function addOption(optionContainer) {
  var optionCount = optionContainer.children.length + 1;

  var optionDiv = document.createElement('div');
  optionDiv.className = 'option';

  var optionInput = document.createElement('input');
  optionInput.type = 'text';
  optionInput.name = 'option' + optionContainer.dataset.questionId;
  optionInput.required = true;

  var removeOptionButton = document.createElement('button');
  removeOptionButton.type = 'button';
  removeOptionButton.className = 'remove-option-btn';
  removeOptionButton.textContent = 'Remove Option';
  removeOptionButton.addEventListener('click', function () {
    optionContainer.removeChild(optionDiv);
  });

  optionDiv.appendChild(optionInput);
  optionDiv.appendChild(removeOptionButton);

  optionContainer.appendChild(optionDiv);
}

// Function to add a new question section
function addQuestion() {
  var questionsContainer = document.getElementById('questions-container');
  var questionCount = questionsContainer.children.length + 1;

  var questionDiv = document.createElement('div');
  questionDiv.className = 'question';

  var questionLabel = document.createElement('label');
  questionLabel.textContent = 'Question ' + questionCount + ':';

  var questionInput = document.createElement('input');
  questionInput.type = 'text';
  questionInput.name = 'question' + questionCount;
  questionInput.required = true;

  var typeLabel = document.createElement('label');
  typeLabel.textContent = 'Question Type:';

  var typeSelect = document.createElement('select');
  typeSelect.name = 'type' + questionCount;

  var multipleChoiceOption = document.createElement('option');
  multipleChoiceOption.value = 'multiple-choice';
  multipleChoiceOption.textContent = 'Multiple Choice';

  var shortAnswerOption = document.createElement('option');
  shortAnswerOption.value = 'short-answer';
  shortAnswerOption.textContent = 'Short Answer';

  typeSelect.appendChild(multipleChoiceOption);
  typeSelect.appendChild(shortAnswerOption);

  var optionsContainer = document.createElement('div');
  optionsContainer.className = 'options';
  optionsContainer.dataset.questionId = questionCount;

  var optionLabel = document.createElement('label');
  optionLabel.textContent = 'Options:';

  var optionInput = document.createElement('input');
  optionInput.type = 'text';
  optionInput.name = 'option' + questionCount;
  optionInput.required = true;

  var addOptionButton = document.createElement('button');
  addOptionButton.type = 'button';
  addOptionButton.className = 'add-option-btn';
  addOptionButton.textContent = 'Add Option';
  addOptionButton.addEventListener('click', function () {
    addOption(optionsContainer);
  });

  optionsContainer.appendChild(optionLabel);
  optionsContainer.appendChild(optionInput);
  optionsContainer.appendChild(addOptionButton);

  questionDiv.appendChild(questionLabel);
  questionDiv.appendChild(questionInput);
  questionDiv.appendChild(typeLabel);
  questionDiv.appendChild(typeSelect);
  questionDiv.appendChild(optionsContainer);

  questionsContainer.appendChild(questionDiv);
}

// Event listener to add question on button click
var addQuestionButton = document.getElementById('add-question-btn');
addQuestionButton.addEventListener('click', addQuestion);
