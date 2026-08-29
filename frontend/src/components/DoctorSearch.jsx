import "./DoctorSearch.css";

function DoctorSearch({ searchTerm, onSearchChange }) {
  return (
    <div className="doctor-search">
      <input
        type="text"
        placeholder="Search by doctor, specialization, or hospital..."
        value={searchTerm}
        onChange={(event) => onSearchChange(event.target.value)}
      />
    </div>
  );
}

export default DoctorSearch;