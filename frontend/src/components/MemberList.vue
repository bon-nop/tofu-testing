<template>
    <v-container fluid>
        <div class="d-flex justify-end">
            <v-btn color="#1B5E20" class="mx-2" @click="onExport()">
                excel
            </v-btn>
            <MemberCreate />
        </div>
        <v-table>
            <thead>
                <tr>
                    <th class="text-left">
                        #
                    </th>
                    <th class="text-left">
                        ชื่อจริง
                    </th>
                    <th class="text-left">
                        นามสกุล
                    </th>
                    <th class="text-left">
                        ตำแหน่ง
                    </th>
                    <th class="text-left">
                        ที่อยู่
                    </th>
                    <th class="text-left">
                        เงินเดือน
                    </th>
                    <th title="action"></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in members" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.first_name }}</td>
                    <td>{{ item.last_name }}</td>
                    <td>{{ item.position }}</td>
                    <td>{{ item.address }}</td>
                    <td>{{ item.expect_salary }}</td>
                    <td>
                        <MemberEdit :memberData="item" />
                        <v-btn color="#EF5350" prepend-icon="mdi-delete-outline" class="mx-2" @click="delMember(item.id)">
                            ลบ
                        </v-btn>
                        <v-btn color="#1B5E20" class="mx-2" @click="onExportOnce(item.id)">
                            excel
                        </v-btn>
                    </td>
                </tr>
            </tbody>
        </v-table>
    </v-container>
</template>
  
<script>
import { ref, reactive } from 'vue';
import { getMembers, deleteMember, downloadMembersExcel, downloadMemberOnceExcel } from "@/hooks/useDesserts.js"
import MemberCreate from './MemberCreate.vue';
import MemberEdit from './MemberEdit.vue';

export default {

    components: {
        MemberCreate,
        MemberEdit
    },

    setup() {

        // Function to delete member
        const delMember = (member_id) => {

            deleteMember(member_id);
        }

        const onExport = () => {
            downloadMembersExcel();
        }

        const onExportOnce = (member_id) => {
            downloadMemberOnceExcel(member_id);
        }

        // Get the list of members
        const { members } = getMembers();

        return { members, onExport, delMember, MemberCreate, onExportOnce };
    },
};
</script>
  