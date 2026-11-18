// src/components/LikeButton.jsx
import React, { useState } from 'react';

export function LikeButton({ label, initialLikes = 0 }) {
  const [likes, setLikes] = useState(initialLikes);

  const handleLike = () => {
    setLikes(prev => prev + 1);
  };

  const handleReset = () => {
    setLikes(0);
  };

  return (
    <div className="like-card">
      <div className="like-header">
        <span className="like-label">{label}</span>
        <span className="like-badge">❤️ {likes}</span>
      </div>
      <div className="btn-group">
        <button onClick={handleLike} className="btn-like">
          👍 Поставить лайк
        </button>
        <button onClick={handleReset} className="btn-reset">
          Сброс
        </button>
      </div>
    </div>
  );
}

// src/App.jsx
export default function App() {
  return (
    <div className="app-container">
      <h2>Лабораторная работа №11 (Вариант 1)</h2>
      <p className="subtitle">Компонент LikeButton: передача подписи через props, счетчик в state</p>

      {/* Демонстрация независимости двух экземпляров */}
      <div className="cards-grid">
        <LikeButton label="Статья: Введение в React" initialLikes={5} />
        <LikeButton label="Урок: Props и State" initialLikes={12} />
      </div>
    </div>
  );
}