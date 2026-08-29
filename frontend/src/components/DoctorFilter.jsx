import "./DoctorFilter.css";

function DoctorFilter({
  selectedSpecialization,
  onSpecializationChange,
}) {
  return (
    <div className="doctor-filter">
      <select
        value={selectedSpecialization}
        onChange={(event) =>
          onSpecializationChange(event.target.value)
        }
      >
        <option value="All">All Specializations</option>
        <option value="Cardiologist">Cardiologist</option>
        <option value="Neurologist">Neurologist</option>
      </select>
    </div>
  );
}

export default DoctorFilter;