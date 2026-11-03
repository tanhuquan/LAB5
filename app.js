// Dữ liệu mẫu ban đầu
const initialStudents = [
  { id: "SV001", name: "Nguyễn Văn An", className: "21DTH01", gpa: 8.6 },
  { id: "SV002", name: "Trần Thị Bích", className: "21DTH02", gpa: 7.2 },
  { id: "SV003", name: "Lê Hoàng Long", className: "21DTH01", gpa: 6.0 }
];

let students = JSON.parse(localStorage.getItem("students")) || initialStudents;

const form = document.getElementById("student-form");
const studentIndexInput = document.getElementById("student-index");
const studentIdInput = document.getElementById("student-id");
const studentNameInput = document.getElementById("student-name");
const studentClassInput = document.getElementById("student-class");
const studentGpaInput = document.getElementById("student-gpa");
const formTitle = document.getElementById("form-title");
const btnCancel = document.getElementById("btn-cancel");
const studentList = document.getElementById("student-list");
const totalStudents = document.getElementById("total-students");
const searchBox = document.getElementById("search-box");

function saveToLocalStorage() {
  localStorage.setItem("students", JSON.stringify(students));
}

function getRank(gpa) {
  if (gpa >= 8.5) return { text: "Xuất sắc", class: "badge-excellent" };
  if (gpa >= 7.0) return { text: "Khá", class: "badge-good" };
  if (gpa >= 5.0) return { text: "Trung bình", class: "badge-average" };
  return { text: "Yếu", class: "badge-weak" };
}

function renderStudents(filterText = "") {
  studentList.innerHTML = "";
  const filter = filterText.toLowerCase();

  const filtered = students.filter(s =>
    s.name.toLowerCase().includes(filter) || s.id.toLowerCase().includes(filter)
  );

  totalStudents.textContent = filtered.length;

  if (filtered.length === 0) {
    studentList.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #888;">Không có dữ liệu sinh viên</td></tr>`;
    return;
  }

  filtered.forEach((student, index) => {
    const rank = getRank(student.gpa);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td><strong>${student.id}</strong></td>
      <td>${student.name}</td>
      <td>${student.className}</td>
      <td>${Number(student.gpa).toFixed(1)}</td>
      <td><span class="badge ${rank.class}">${rank.text}</span></td>
      <td>
        <button class="btn btn-edit" onclick="editStudent(${index})">Sửa</button>
        <button class="btn btn-danger" onclick="deleteStudent(${index})">Xóa</button>
      </td>
    `;
    studentList.appendChild(tr);
  });
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const id = studentIdInput.value.trim();
  const name = studentNameInput.value.trim();
  const className = studentClassInput.value.trim();
  const gpa = parseFloat(studentGpaInput.value);

  const editIndex = studentIndexInput.value;

  if (editIndex === "") {
    // Thêm mới
    students.push({ id, name, className, gpa });
  } else {
    // Cập nhật
    students[editIndex] = { id, name, className, gpa };
    studentIndexInput.value = "";
    formTitle.textContent = "Thêm sinh viên mới";
    btnCancel.style.display = "none";
  }

  saveToLocalStorage();
  form.reset();
  renderStudents(searchBox.value);
});

window.editStudent = function (index) {
  const student = students[index];
  studentIndexInput.value = index;
  studentIdInput.value = student.id;
  studentNameInput.value = student.name;
  studentClassInput.value = student.className;
  studentGpaInput.value = student.gpa;

  formTitle.textContent = "Chỉnh sửa thông tin sinh viên";
  btnCancel.style.display = "inline-block";
};

window.deleteStudent = function (index) {
  if (confirm(`Bạn có chắc muốn xóa sinh viên ${students[index].name}?`)) {
    students.splice(index, 1);
    saveToLocalStorage();
    renderStudents(searchBox.value);
  }
};

btnCancel.addEventListener("click", () => {
  form.reset();
  studentIndexInput.value = "";
  formTitle.textContent = "Thêm sinh viên mới";
  btnCancel.style.display = "none";
});

searchBox.addEventListener("input", (e) => {
  renderStudents(e.target.value);
});

// Khởi chạy hiển thị lần đầu
renderStudents();
