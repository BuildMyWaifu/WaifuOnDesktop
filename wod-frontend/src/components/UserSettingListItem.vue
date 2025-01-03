<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-dialog max-width="800">
        <template v-slot:activator="{ props }">
            <v-list-item v-bind="props">
                <v-list-item-title>設定</v-list-item-title>
            </v-list-item>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title class="text-h5">
                    <v-row class="align-center">
                        <v-col>設定</v-col>
                        <v-col class="text-end">
                            <v-btn flat icon="mdi-close" @click="isActive.value = false" />
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                    <v-row>
                        <!-- Left Navigation List -->
                        <v-col cols="3">
                            <v-list>
                                <v-list-item v-for="(item, index) in navigationItems" :key="index"
                                    :class="{ 'selected-nav-item': selectedItem === index }" @click="selectItem(index)">
                                    <template v-slot:prepend>
                                        <v-icon>{{ item.icon }}</v-icon>
                                    </template>
                                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-col>

                        <!-- Right Content Area -->
                        <v-col cols="9">
                            <div v-if="false"> <!-- 由於現階段沒有用到，刪掉又很可惜，所以就先留著 -->
                                <div class="text-h6">一般</div>
                                <p>不需要就刪除</p>
                            </div>
                            <div v-else-if="selectedItem === 0">
                                <v-card flat>
                                    <v-text-field v-model="name" class="mx-2" label="姓名" rows="1"></v-text-field>
                                    <v-text-field v-model="email" class="mx-2" label="電子郵件" rows="1"></v-text-field>

                                    <v-card-actions>
                                        <v-spacer></v-spacer> <!-- 讓按鈕靠右 -->
                                        <v-btn @click="changeNameEmail" rounded="xl">儲存</v-btn>
                                    </v-card-actions>

                                </v-card>
                            </div>
                            <div v-else-if="selectedItem === 1">
                                <v-card flat>
                                    <v-card-text class="d-flex justify-space-between align-center">
                                        修改密碼
                                        <v-btn @click="openChangePwdDialog" rounded="xl">修改</v-btn>
                                    </v-card-text>

                                    <v-card-text class="d-flex justify-space-between align-center">
                                        刪除帳號
                                        <v-btn @click="openDeleteAccountDialog" rounded="xl">刪除</v-btn>
                                    </v-card-text>
                                </v-card>
                                <!-- 密碼修改對話框 -->
                                <v-dialog v-model="isChangePwdDialogOpen" max-width="500">
                                    <v-card flat>
                                        <v-card-title class="text-h5">更改密碼</v-card-title>
                                        <v-card-text>
                                            <v-form ref="form" v-model="isValid">
                                                <v-text-field v-model="newPassword" label="新密碼" type="password"
                                                    :rules="[rules.required, rules.minLength]" clearable></v-text-field>
                                                <v-text-field v-model="confirmPassword" label="確認新密碼" type="password"
                                                    :rules="[rules.matchPassword]" clearable></v-text-field>
                                            </v-form>
                                        </v-card-text>
                                        <v-card-actions>
                                            <v-btn @click="closeChangePwdDialog">取消</v-btn>
                                            <v-spacer></v-spacer>
                                            <v-btn color="primary" :disabled="!isValid"
                                                @click="submitChangePwd">儲存</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>

                                <v-dialog v-model="isDeleteAccountDialogOpen" max-width="500">
                                    <v-card flat>
                                        <v-card-title>確認要刪除帳號嗎?</v-card-title>
                                        <v-card-actions>
                                            <v-btn @click="closeDeleteAccountDialog">取消</v-btn>
                                            <v-spacer></v-spacer>
                                            <v-btn color="primary" @click="deleteAccount">確定</v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </div>
                            <div v-else>
                                <div class="text-h6">尚未定義的設定頁面</div>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>
    <v-snackbar v-model="snackbar" :timeout="2000" color="success">
        <v-icon class="me-2">mdi-check-circle</v-icon>
        已儲存成功
    </v-snackbar>
</template>

<script lang="ts" setup>
    import { ref } from 'vue';
    import { useAppStore } from '@/stores/app';
    import { deleteApi, handleErrorAlert, patchApi, postApi } from '@/utils/api';
    import { useRouter } from 'vue-router';
    import { User } from '@/utils/model';
    import { hash } from '@/utils/utils';

    const store = useAppStore();
    const selectedItem = ref(0);
    const snackbar = ref(false);
    const name = ref(store.user?.profile.name || '');
    const email = ref(store.user?.profile.email || '');
    const isChangePwdDialogOpen = ref(false);
    const isDeleteAccountDialogOpen = ref(false);

    const isValid = ref(false);
    const newPassword = ref('');
    const confirmPassword = ref('');

    const navigationItems = [
        // { title: '一般', icon: 'mdi-cog' },
        { title: '個人化', icon: 'mdi-account' },
        { title: '安全性', icon: 'mdi-lock' },
    ];

    const selectItem = (index: number) => {
        selectedItem.value = index;
    };

    const changeNameEmail = async () => {
        const user = handleErrorAlert(await patchApi("/me", {
            name: name.value,
            email: email.value,
        })) as User
        if (user) {
            snackbar.value = true;
            await store.login(user)
        }
        // console.log(' store.user.profile.name = ', store.user?.profile.name);
        // console.log(' store.user.profile.email = ', store.user?.profile.email);
    };

    const rules = {
        required: (value: string) => !!value || '此欄位必填',
        minLength: (value: string) =>
            value.length >= 6 || '密碼至少需要6個字元',
        matchPassword: (value: string) =>
            value === newPassword.value || '密碼不相符',
    };

    const openChangePwdDialog = () => {
        isChangePwdDialogOpen.value = true;
    };

    const closeChangePwdDialog = () => {
        isChangePwdDialogOpen.value = false;
    };

    const submitChangePwd = async () => {
        const res = await postApi(`/user/${store.user?._id}/password`, {
            password: hash(newPassword.value),
        });
        alert(res.message)
        // 這裡可以進行後端請求來更新密碼
        closeChangePwdDialog();
    };

    const openDeleteAccountDialog = () => {
        isDeleteAccountDialogOpen.value = true;
    };

    const closeDeleteAccountDialog = () => {
        isDeleteAccountDialogOpen.value = false;

    };
    const router = useRouter();
    const deleteAccount = async () => {
        // API
        const res = await deleteApi("/me")
        alert(res.message)
        await store.logout();
        router.push("/");
        isDeleteAccountDialogOpen.value = false;
    };


</script>
