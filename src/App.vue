<script setup>
import Header from './components/Header.vue'
import Home from './views/Home.vue'
</script>

<template>
  <el-container>
    <Header />
    <el-main>
      <Home />
    </el-main>
  </el-container>
</template>

<style>
.el-main {
  padding: 0;
}
</style>
