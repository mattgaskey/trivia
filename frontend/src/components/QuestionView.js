import React, { useState, useEffect, useCallback } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';

const QuestionView = () => {
  const [questions, setQuestions] = useState([]);
  const [page, setPage] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [categories, setCategories] = useState({});
  const [currentCategory, setCurrentCategory] = useState(null);

  const getQuestions = useCallback(async () => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    try {
      const response = await fetch(`${apiBaseUrl}/questions?page=${page}`);
      const result = await response.json();
      setQuestions(result.questions);
      setTotalQuestions(result.total_questions);
      setCategories(result.categories);
      setCurrentCategory(result.current_category);
    } catch (error) {
      alert('Unable to load questions. Please try your request again');
    }
  }, [page]);

  useEffect(() => {
    getQuestions();
  }, [getQuestions]);

  const selectPage = useCallback((num) => {
    setPage(num);
  }, []);

  const createPagination = () => {
    let pageNumbers = [];
    let maxPage = Math.ceil(totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === page ? 'active' : ''} clickable`}
          onClick={() => selectPage(i)}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  };

  const getByCategory = async (id) => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    try {
      const response = await fetch(`${apiBaseUrl}/categories/${id}/questions`);
      const result = await response.json();
      setQuestions(result.questions);
      setTotalQuestions(result.total_questions);
      setCurrentCategory(result.current_category);
    } catch (error) {
      alert('Unable to load questions. Please try your request again');
    }
  };

  const submitSearch = async (searchTerm) => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    try {
      const response = await fetch(`${apiBaseUrl}/questions/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchTerm: searchTerm }),
      });
      const result = await response.json();
      setQuestions(result.questions);
      setTotalQuestions(result.total_questions);
      setCurrentCategory(result.current_category);
    } catch (error) {
      alert('Unable to load questions. Please try your request again');
    }
  };

  const questionAction = (id) => async (action) => {
    const apiBaseUrl = process.env.REACT_APP_API_BASE_URL;
    if (action === 'DELETE') {
      if (window.confirm('Are you sure you want to delete the question?')) {
        try {
          await fetch(`${apiBaseUrl}/questions/${id}`, {
            method: 'DELETE',
          });
          getQuestions();
        } catch (error) {
          alert('Unable to load questions. Please try your request again');
        }
      }
    }
  };

  return (
    <div className='question-view'>
      <div className='categories-list'>
        <h2 className='clickable' onClick={getQuestions}>Categories</h2>
        <ul>
          {Object.keys(categories).map((id) => (
            <li key={id} className='clickable' onClick={() => getByCategory(id)}>
              <img
                className='category'
                alt={`${categories[id].toLowerCase()}`}
                src={`${categories[id].toLowerCase()}.svg`}
              />
              {categories[id]}
            </li>
          ))}
        </ul>
        <Search submitSearch={submitSearch} />
      </div>
      <div className='questions-list'>
        <h2>Questions</h2>
        {questions.map((q) => (
          <Question
            key={q.id}
            question={q.question}
            answer={q.answer}
            category={categories[q.category]}
            difficulty={q.difficulty}
            questionAction={questionAction(q.id)}
          />
        ))}
        <div className='pagination-menu'>{createPagination()}</div>
      </div>
    </div>
  );
};

export default QuestionView;