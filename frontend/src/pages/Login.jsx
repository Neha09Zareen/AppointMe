function Login() {
  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Login button clicked!");
  };

  return (
    <div>
      <h1>Hospital Appointment System</h1>

      <h2>Login</h2>

      <form onSubmit={handleSubmit}>
        <label>Email</label>
        <br />
        <input type="email" placeholder="Enter your email" />

        <br /><br />

        <label>Password</label>
        <br />
        <input type="password" placeholder="Enter your password" />

        <br /><br />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;