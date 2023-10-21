<template>
    <v-btn color="#5865f2" prepend-icon="mdi-plus" @click="dialog = true">
        เพิ่มรายการ
    </v-btn>
    <v-dialog v-model="dialog" width="1024">
        <v-card>
            <v-card-title>
                <span class="text-h5">เพิ่มข้อมูลผู้สมัคร</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <v-text-field v-model="firstName" label="ชื่อจริง*" required></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <v-text-field v-model="lastName" label="นามสกุล*" required></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <v-text-field v-model="position" label="ตำแหน่ง*" required></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <v-text-field v-model="salary" label="เงินเดือน*" type="number" required></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-text-field v-model="address" label="ที่อยู่"></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="dialog = false">
                    ปิด
                </v-btn>
                <v-btn color="blue-darken-1" variant="text" @click="saveMember">
                    บันทึก
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { ref } from 'vue';
import { createMember } from '@/hooks/useDesserts';

export default {
    setup() {
        const firstName = ref("");
        const lastName = ref("");
        const position = ref("");
        const salary = ref("");
        const address = ref("");
        const dialog = ref(false);

        const saveMember = () => {
            const newMember = {
                first_name: firstName.value,
                last_name: lastName.value,
                position: position.value,
                expect_salary: salary.value,
                address: address.value,
            };

            createMember(newMember);

            firstName.value = '';
            lastName.value = '';
            position.value = '';
            salary.value = '';
            address.value = '';
            dialog.value = false;
        }

        return { firstName, lastName, position, salary, address, saveMember, dialog }
    }
}
</script>

<style></style>