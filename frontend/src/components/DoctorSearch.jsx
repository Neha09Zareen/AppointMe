import "./DoctorSearch.css";

function DoctorSearch({ searchTerm, onSearchChange }) {
  return (
    <div className="doctor-search">
      <input
        type="text"
        placeholder="Search for doctors or specialization..."
        value={searchTerm}
        onChange={(event) => onSearchChange(event.target.value)}
      />
    </div>
  );
}

export default DoctorSearch;