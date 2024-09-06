import React, { useState, useEffect } from 'react';
import '../stylesheets/FormView.css';

const FormView = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [difficulty, setDifficulty] = useState(1);
  const [category, setCategory] = useState(1);
  const [categories, setCategories] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

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

  const submitQuestion = async (event) => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    event.preventDefault();
    try {
      const response = await fetch(`${apiBaseUrl}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          answer,
          difficulty,
          category,
        }),
      });
      if (response.ok) {
        document.getElementById('add-question-form').reset();
        setQuestion('');
        setAnswer('');
        setDifficulty(1);
        setCategory(1);
        setSuccessMessage('Question added successfully!');
        setTimeout(() => setSuccessMessage(''), 3000); // Clear message after 3 seconds
      } else {
        throw new Error('Unable to add question');
      }
    } catch (error) {
      alert('Unable to add question. Please try your request again');
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    switch (name) {
      case 'question':
        setQuestion(value);
        break;
      case 'answer':
        setAnswer(value);
        break;
      case 'difficulty':
        setDifficulty(Number(value));
        break;
      case 'category':
        setCategory(Number(value));
        break;
      default:
        break;
    }
  };

  return (
    <div id='add-form'>
      <h2>Add a New Trivia Question</h2>
      {successMessage && <p className='success-message'>{successMessage}</p>}
      <form
        className='form-view'
        id='add-question-form'
        onSubmit={submitQuestion}
      >
        <label>
          Question
        </label>
        <input
          type='text'
          name='question'
          onChange={handleChange}
        />
        <label>
          Answer
        </label>
        <input
          type='text'
          name='answer'
          onChange={handleChange}
        />
        <label>
          Difficulty
        </label>
        <select
          name='difficulty'
          onChange={handleChange}
        >
          <option value='1'>1</option>
          <option value='2'>2</option>
          <option value='3'>3</option>
          <option value='4'>4</option>
          <option value='5'>5</option>
        </select>
        <label>
          Category
        </label>
        <select
          name='category'
          onChange={handleChange}
        >
          {Object.keys(categories).map((id) => (
            <option key={id} value={id}>
              {categories[id]}
            </option>
          ))}
        </select>
        <input type='submit' className='button clickable' value='Submit' />
      </form>
    </div>
  );
}

export default FormView;