import React, { useState } from "react";

function AddTask() {
  const [formData, setFormData] = useState({
    route: "",
    driver_id: "",
    car_id: "",
  });
  const [response, setResponse] = useState('');

  // Обработчик изменения данных в форме
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Проверка на пустые значения
  const validateForm = () => {
    const { route, driver_id, car_id } = formData;
    if (!route || !driver_id || !car_id) {
      setResponse('Error: All fields must be filled out.');
      return false;
    }
    return true;
  };

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const res = await fetch('http://127.0.0.1:8000/tasks/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setResponse(`Task added successfully! ID: ${data['New task added'].id}`);
      } else {
        setResponse(`Error: ${data.detail}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('An unexpected error occurred.');
    }
  };

  return (
    <div className="add-task">
      <h2>Add New Task</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="route">Route:</label>
        <input
          type="text"
          id="route"
          name="route"
          value={formData.route}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="driver_id">Driver ID:</label>
        <input
          type="number"
          id="driver_id"
          name="driver_id"
          value={formData.driver_id}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="car_id">Vehicle ID:</label>
        <input
          type="number"
          id="car_id"
          name="car_id"
          value={formData.car_id}
          onChange={handleChange}
          required
        />
        <br />
        <button type="submit">Add Task</button>
      </form>
      <p>{response}</p> {/* Просто выводим сообщение ниже формы */}
    </div>
  );
}

export default AddTask;
