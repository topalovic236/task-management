import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/auth/login';
import Register from './components/auth/register';
import TaskList from './components/users/UserTaskList';
import Profile from './components/users/Profile';
import AdminUserList from './components/admin/AdminUserLIst';
import AdminTaskList from './components/admin/AdminTaskList';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/tasks" element={<TaskList />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin/users" element={<AdminUserList />} />
        <Route path="/admin/tasks" element={<AdminTaskList />} />
      </Routes>
    </Router>
  );
};

export default App;
