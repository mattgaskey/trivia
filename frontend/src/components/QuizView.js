import React, { useState, useEffect, useCallback } from 'react';
import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

const QuizView = () => {
  const [quizCategory, setQuizCategory] = useState(null);
  const [previousQuestions, setPreviousQuestions] = useState([]);
  const [showAnswer, setShowAnswer] = useState(false);
  const [categories, setCategories] = useState({});
  const [numCorrect, setNumCorrect] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [guess, setGuess] = useState('');
  const [forceEnd, setForceEnd] = useState(false);
  const [noMoreQuestions, setNoMoreQuestions] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    try {
      const response = await fetch(`${apiBaseUrl}/categories`);
      const result = await response.json();
      setCategories(result.categories);
    } catch (error) {
      alert('Unable to load categories. Please try your request again');
    }
  };

  const getNextQuestion = useCallback(async (category) => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    const newPreviousQuestions = [...previousQuestions];
    if (currentQuestion && currentQuestion.id) {
      newPreviousQuestions.push(currentQuestion.id);
    }

    try {
      const response = await fetch(`${apiBaseUrl}/quizzes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          previous_questions: newPreviousQuestions,
          quiz_category: category || quizCategory,
        }),
      });
      const result = await response.json();
      if (result.question) {
        setCurrentQuestion(result.question);
        setShowAnswer(false);
        setPreviousQuestions(newPreviousQuestions);
        setGuess(''); // Clear the guess input
      } else {
        setNoMoreQuestions(true);
      }
    } catch (error) {
      alert('Unable to load next question. Please try your request again');
    }
  }, [previousQuestions, currentQuestion, quizCategory]);

  const selectCategory = useCallback(({ type, id = 0 }) => {
    setQuizCategory({ type, id });
    getNextQuestion({ type, id });
  }, [getNextQuestion]);

  const handleChange = (event) => {
    setGuess(event.target.value);
  };

  const submitGuess = (event) => {
    event.preventDefault();
    const evaluate = evaluateAnswer();
    setNumCorrect((prevNumCorrect) => (evaluate ? prevNumCorrect + 1 : prevNumCorrect));
    setShowAnswer(true);
  };

  const restartGame = () => {
    setQuizCategory(null);
    setPreviousQuestions([]);
    setShowAnswer(false);
    setNumCorrect(0);
    setCurrentQuestion(null);
    setGuess('');
    setForceEnd(false);
    setNoMoreQuestions(false);
  };

  const evaluateAnswer = () => {
    if (!currentQuestion) return false;
    const formatGuess = guess
      .replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '')
      .toLowerCase();
    const answerArray = currentQuestion.answer
      .toLowerCase()
      .split(' ');
    return answerArray.every((el) => formatGuess.includes(el));
  };

  const renderPrePlay = () => (
    <div className='quiz-play-holder'>
      <div className='choose-header'>Choose Category</div>
      <div className='category-holder'>
        <div className='play-category' onClick={() => selectCategory({ type: 'ALL', id: 0 })}>
          ALL
        </div>
        {Object.keys(categories).map((id) => (
          <div
            key={id}
            value={id}
            className='play-category'
            onClick={() => selectCategory({ type: categories[id], id })}
          >
            {categories[id]}
          </div>
        ))}
      </div>
    </div>
  );

  const renderFinalScore = () => (
    <div className='quiz-play-holder'>
      <div className='final-header'>Your Final Score is {numCorrect}</div>
      <div className='play-again button' onClick={restartGame}>
        Play Again?
      </div>
    </div>
  );
  
  const renderNoMoreQuestions = () => (
    <div className='quiz-play-holder'>
      <div className='final-header'>No more questions available.</div>
      <div className='show-score button' onClick={() => setForceEnd(true)}>
        Show Final Score
      </div>
    </div>
  );
  
  const renderCorrectAnswer = () => {
    const evaluate = evaluateAnswer();
    return (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>{currentQuestion?.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>
          {evaluate ? 'You were correct!' : 'You were incorrect'}
        </div>
        <div className='quiz-answer'>{currentQuestion?.answer}</div>
        <div className='next-question button' onClick={() => getNextQuestion()}>
          Next Question
        </div>
      </div>
    );
  };
  
  const renderPlay = () => {
    if (forceEnd) {
      return renderFinalScore();
    }
  
    if (noMoreQuestions) {
      return renderNoMoreQuestions();
    }
  
    if (previousQuestions.length === questionsPerPlay) {
      return renderFinalScore();
    }
  
    if (showAnswer) {
      return renderCorrectAnswer();
    }
  
    return (
      <div className='quiz-play-holder'>
        <div className='quiz-question'>{currentQuestion?.question}</div>
        <form onSubmit={submitGuess}>
          <input type='text' name='guess' value={guess} onChange={handleChange} />
          <input className='submit-guess' type='submit' value='Submit Answer' />
        </form>
      </div>
    );
  };
  
  return quizCategory ? renderPlay() : renderPrePlay();
  };
  
  export default QuizView;