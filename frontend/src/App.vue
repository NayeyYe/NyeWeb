<script setup>
import Header from './components/Header.vue'
</script>

<template>
  <el-container>
    <Header />
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<style>
.el-main {
  padding: 0;
}
</style>
