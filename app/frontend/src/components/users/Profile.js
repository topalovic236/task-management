import React, { useState, useEffect } from 'react';
import { getUser } from '../../services/api';

const Profile = () => {
  const [user, setUser] = useState({});

  useEffect(() => {
    const fetchUser = async () => {
      const userId = localStorage.getItem('userId');
      const userData = await getUser(userId);
      setUser(userData);
    };
    fetchUser();
  }, []);

  return (
    <div>
      <h2>User Profile</h2>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
    </div>
  );
};

export default Profile;