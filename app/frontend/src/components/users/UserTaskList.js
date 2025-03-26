import React, { useState, useEffect } from 'react';
import { getAllTasks } from '../../services/api';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      const userId = localStorage.getItem('userId'); 
      const tasksData = await getAllTasks(userId);
      setTasks(tasksData);
    };
    fetchTasks();
  }, []);

  return (
    <div>
      <h2>Your Tasks</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            {task.title} - {task.description}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;