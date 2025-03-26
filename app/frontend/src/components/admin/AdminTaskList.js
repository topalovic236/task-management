import React, { useState, useEffect } from 'react';
import { getAllTasks } from '../../services/api';

const AdminTaskList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      const tasksData = await getAllTasks();
      setTasks(tasksData);
    };
    fetchTasks();
  }, []);

  return (
    <div>
      <h2>Admin - All Tasks</h2>
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

export default AdminTaskList;
