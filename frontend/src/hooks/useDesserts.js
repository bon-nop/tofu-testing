import { ref, reactive } from 'vue';
import axios from 'axios';

const backendUrl = 'http://localhost:8000';

function useDesserts() {

  const desserts = reactive([
    {
      name: 'Frozen Yogurt',
      calories: 159,
    },
    {
      name: 'Ice cream sandwich',
      calories: 237,
    },
    {
      name: 'Eclair',
      calories: 262,
    },
    {
      name: 'Cupcake',
      calories: 305,
    },
    {
      name: 'Gingerbread',
      calories: 356,
    },
    {
      name: 'Jelly bean',
      calories: 375,
    },
    {
      name: 'Lollipop',
      calories: 392,
    },
    {
      name: 'Honeycomb',
      calories: 408,
    },
    {
      name: 'Donut',
      calories: 452,
    },
    {
      name: 'KitKat',
      calories: 518,
    },
  ]);

  return { desserts };
}

const members = ref([]);

function getMembers() {
  axios.get(`${backendUrl}/members`)
    .then((response) => {
      members.value = response.data;
    })
    .catch((error) => {
      console.error('Error fetching members:', error);
    });

  return { members };
}

function downloadMembersExcel() {
  // Create a link element
  const link = document.createElement('a');
  link.style.display = 'none';

  // Make a GET request to download the Excel file
  axios
    .get(`${backendUrl}/export`, { responseType: 'blob' }) // Set responseType to 'blob' for binary data
    .then((response) => {
      // Create a blob URL from the binary data
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);

      // Set the link's attributes
      link.href = url;
      link.download = 'members.xlsx';

      // Simulate a click on the link to trigger the download
      document.body.appendChild(link);
      link.click();

      // Clean up
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error('Error fetching members:', error);
    });
}

function downloadMemberOnceExcel(member_id) {
  // Create a link element
  const link = document.createElement('a');
  link.style.display = 'none';

  // Make a GET request to download the Excel file
  axios
    .get(`${backendUrl}/export/${member_id}`, { responseType: 'blob' }) // Set responseType to 'blob' for binary data
    .then((response) => {
      // Create a blob URL from the binary data
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);

      // Set the link's attributes
      link.href = url;
      link.download = `member_${member_id}.xlsx`;

      // Simulate a click on the link to trigger the download
      document.body.appendChild(link);
      link.click();

      // Clean up
      window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error('Error fetching members:', error);
    });
}


function createMember(newMember) {
  axios
    .post(`${backendUrl}/members`, newMember)
    .then((response) => {
      
      console.log('New member added:', response.data);
      getMembers();
    })
    .catch((error) => {
      console.error('Error adding a new member:', error);
    });
}

function updateMember(newMember, member_id) {
  axios
    .put(`${backendUrl}/members/${member_id}`, newMember)
    .then((response) => {
      
      console.log('Update member data:', response.data);
      getMembers();
    })
    .catch((error) => {
      console.error('Error editing member:', error);
    });
}

function deleteMember(member_id) {
  axios
    .delete(`${backendUrl}/members/${member_id}`)
    .then((response) => {
      
      console.log(response.data.message);
      getMembers();
    })
    .catch((error) => {
      console.error('Error delete member:', error);
    });

}

export { useDesserts, getMembers, createMember, updateMember, deleteMember, downloadMembersExcel, downloadMemberOnceExcel };
