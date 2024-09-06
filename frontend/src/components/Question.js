import React, { useState } from 'react';
import '../stylesheets/Question.css';

const Question = ({ question, answer, category, difficulty, questionAction }) => {
  const [visibleAnswer, setVisibleAnswer] = useState(false);

  const flipVisibility = () => {
    setVisibleAnswer(!visibleAnswer);
  };

  return (
    <div className='Question-holder'>
      <div className='Question-status'>
        <img
          className='category'
          alt={`${category.toLowerCase()}`}
          src={`${category.toLowerCase()}.svg`}
        />
        <img
          src='delete.png'
          alt='delete'
          className='delete clickable'
          onClick={() => questionAction('DELETE')}
        />
      </div>
      <div className='Question'>{question}</div>
      <div className='Question-footer'>
        <div className='difficulty'>Difficulty: {difficulty}</div>
        <div className='show-answer clickable' onClick={flipVisibility}>
          {visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
      </div>
      <div className='answer-holder'>
        <span style={{ visibility: visibleAnswer ? 'visible' : 'hidden' }}>
          Answer: {answer}
        </span>
      </div>
    </div>
  );
};

export default Question;