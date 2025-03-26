import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;


export const loginUser = async (loginData) => {
  try {
    const response = await axios.post(`${BASE_URL}/auth/token`, loginData);
    return response.data;  
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

export const getAllTasks = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/tasks`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
      throw error;
    }
  };

export const getUsers = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/users`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch users:', error);
      throw error;
    }
  };

export const getUser = async (userId) => {
    try {
      const response = await axios.get(`${BASE_URL}/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch user with ID ${userId}:`, error);
      throw error;
    }
  };
  