
import "./DoctorFilter.css";

function DoctorFilter({
  selectedSpecialization,
  onSpecializationChange,
  specializations = [],
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

        {specializations.map((specialization) => (
          <option key={specialization} value={specialization}>
            {specialization}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DoctorFilter;