import React, { useState } from 'react';

function AddDriver() {
  const [driverData, setDriverData] = useState({
    name: '',
    experience: '',
    phone: '',
    email: '',
    password: ''
  });
  const [response, setResponse] = useState('');

  // Обработчик изменения данных в форме
  const handleChange = (e) => {
    const { name, value } = e.target;
    setDriverData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Проверка на NaN и пустые значения
  const validateForm = () => {
    const { name, experience, phone, email, password } = driverData;
    if (!name || !experience || !phone || !email || !password) {
      setResponse('Error: All fields must be filled out.');
      return false;
    }
    if (isNaN(experience) || isNaN(phone)) {
      setResponse('Error: Experience and phone must be valid numbers.');
      return false;
    }
    return true;
  };

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const res = await fetch('http://127.0.0.1:8000/drivers/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(driverData),
      });

      const data = await res.json();
      if (res.ok) {
        setResponse(`Driver added successfully! ID: ${data['New driver added'].id}`);
      } else {
        setResponse(`Error: ${data.detail}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('An unexpected error occurred.');
    }
  };

  return (
    <div className="add-driver">
      <h2>Add New Driver</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          value={driverData.name}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="experience">Experience:</label>
        <input
          type="number"
          id="experience"
          name="experience"
          value={driverData.experience}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="phone">Phone:</label>
        <input
          type="tel"
          id="phone"
          name="phone"
          value={driverData.phone}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={driverData.email}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={driverData.password}
          onChange={handleChange}
          required
        />
        <br />
        <button type="submit">Add Driver</button>
      </form>

      <div className="response">
        <p>{response}</p>
      </div>
    </div>
  );
}

export default AddDriver;
