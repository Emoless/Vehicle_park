import React, { useState } from "react";

function AddVehicle() {
  const [formData, setFormData] = useState({
    brand: "",
    reg_num: "",
    mileage: "",
  });
  const [response, setResponse] = useState('');

  // Обработчик изменения данных в форме
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Проверка на пустые значения
  const validateForm = () => {
    const { brand, reg_num, mileage } = formData;
    if (!brand || !reg_num || !mileage) {
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
      const res = await fetch('http://127.0.0.1:8000/vehicles/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (res.ok) {
        setResponse(`Vehicle added successfully! ID: ${data['New vehicle added'].id}`);
      } else {
        setResponse(`Error: ${data.detail}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('An unexpected error occurred.');
    }
  };

  return (
    <div className="add-vehicle">
      <h2>Add New Vehicle</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="brand">Brand:</label>
        <input
          type="text"
          id="brand"
          name="brand"
          value={formData.brand}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="reg_num">Registration Number:</label>
        <input
          type="text"
          id="reg_num"
          name="reg_num"
          value={formData.reg_num}
          onChange={handleChange}
          required
        />
        <br />
        <label htmlFor="mileage">Mileage:</label>
        <input
          type="number"
          id="mileage"
          name="mileage"
          value={formData.mileage}
          onChange={handleChange}
          required
        />
        <br />
        <button type="submit">Add Vehicle</button>
      </form>
      <p>{response}</p> {/* Просто выводим сообщение ниже формы */}
    </div>
  );
}

export default AddVehicle;
