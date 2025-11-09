import { useState, useEffect } from 'react';
import accountsService from '../api/accountsService';

function StudentList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      const response = await accountsService.getStudents();
      setStudents(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch students: ' + err.message);
      console.error('Error fetching students:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading students...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Students</h2>
      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <ul>
          {students.map((student) => (
            <li key={student.id}>
              {student.first_name} {student.last_name} - {student.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default StudentList;
