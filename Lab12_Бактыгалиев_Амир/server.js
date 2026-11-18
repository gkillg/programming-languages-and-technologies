const express = require('express');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Секретный ключ для подписи (в реальных проектах хранится в .env)
const JWT_SECRET = 'super_secret_jwt_key_12345';

const MOCK_USER = {
  username: 'student',
  password: 'password123',
  role: 'student',
  name: 'Иван Иванов'
};

// 1. Эндпоинт входа: генерация JWT
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.status(400).json({ error: 'Поля логина и пароля обязательны.' });
  }

  if (username !== MOCK_USER.username || password !== MOCK_USER.password) {
    return res.status(401).json({ error: 'Неверный логин или пароль.' });
  }

  // Создаем короткоживущий JWT (срок действия 5 минут)
  const payload = {
    sub: 'user_15',
    name: MOCK_USER.name,
    role: MOCK_USER.role
  };

  const token = jwt.sign(payload, JWT_SECRET, { algorithm: 'HS256', expiresIn: '5m' });

  return res.json({
    message: 'Успешный вход',
    token
  });
});

// Middleware для проверки JWT на защищенном эндпоинте
function verifyJWT(req, res, next) {
  const authHeader = req.headers['authorization'];
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Отсутствует токен аутентификации (HTTP 401).' });
  }

  const token = authHeader.split(' ')[1];

  jwt.verify(token, JWT_SECRET, { algorithms: ['HS256'] }, (err, decoded) => {
    if (err) {
      if (err.name === 'TokenExpiredError') {
        return res.status(401).json({ error: 'Срок действия токена истек (TokenExpiredError).' });
      }
      return res.status(403).json({ error: 'Недействительная подпись токена (HTTP 403).' });
    }

    req.user = decoded;
    next();
  });
}

// 2. Защищенный эндпоинт
app.get('/api/protected', verifyJWT, (req, res) => {
  res.json({
    status: 'success',
    message: 'Доступ разрешен! Сервер успешно верифицировал подпись и срок токена.',
    user: req.user,
    serverTime: new Date().toISOString()
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Сервер запущен: http://localhost:${PORT}`);
});