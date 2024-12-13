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
                            <div v-if="false">  <!-- 由於現階段沒有用到，刪掉又很可惜，所以就先留著 -->
                                <div class="text-h6">一般</div>
                                <p>不需要就刪除</p>
                            </div>
                            <div v-else-if="selectedItem === 0">
                                <v-card flat>
                                    <v-textarea class="mx-2" label="用戶ID" rows="1"></v-textarea>
                                    <v-textarea class="mx-2" label="姓名" rows="1"></v-textarea>
                                    <v-textarea class="mx-2" label="Email" rows="1"></v-textarea>

                                    <v-card-actions>
                                        <v-spacer></v-spacer> <!-- 讓按鈕靠右 -->
                                        <v-btn rounded="xl">儲存</v-btn>
                                    </v-card-actions>

                                </v-card>
                            </div>
                            <div v-else-if="selectedItem === 1">
                                <v-card flat>
                                    <v-card-text class="d-flex justify-space-between align-center">
                                        修改密碼
                                        <v-btn rounded="xl">修改</v-btn>
                                    </v-card-text>
                                
                                    <v-card-text class="d-flex justify-space-between align-center">
                                        刪除帳號
                                        <v-btn rounded="xl">刪除</v-btn>
                                    </v-card-text>
                                </v-card>
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
</template>

<script lang="ts" setup>
    import { ref } from 'vue';

    // 接收父組件的 @close 事件

    const selectedItem = ref(0);

    const navigationItems = [
        // { title: '一般', icon: 'mdi-cog' },
        { title: '個人化', icon: 'mdi-account' },
        { title: '安全性', icon: 'mdi-lock' },
    ];

    const selectItem = (index: number) => {
        selectedItem.value = index;
    };


</script>
