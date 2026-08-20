function Register() {
  return (
    <div>
      <h1>Hospital Appointment System</h1>

      <h2>Register</h2>

      <form>
        <label>Full Name</label>
        <br />
        <input type="text" placeholder="Enter your full name" />

        <br /><br />

        <label>Email</label>
        <br />
        <input type="email" placeholder="Enter your email" />

        <br /><br />

        <label>Password</label>
        <br />
        <input type="password" placeholder="Enter your password" />

        <br /><br />

        <button>Register</button>
      </form>
    </div>
  );
}

export default Register;