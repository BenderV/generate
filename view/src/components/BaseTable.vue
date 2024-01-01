<template>
  <div ref="table"></div>
</template>

<script setup>
import { ref, reactive, onMounted, defineProps, watch } from "vue";
import { TabulatorFull as Tabulator } from "tabulator-tables"; //import Tabulator library
import "tabulator-tables/dist/css/tabulator_semanticui.min.css";

const table = ref(null); // reference to your table element
const tabulator = ref(null); // variable to hold your table

const props = defineProps({
  data: {
    type: Array,
    default: [],
  },
});

watch(
  props,
  () => {
    tabulator.value.setData(props.data);
  },
  { deep: true }
);

onMounted(() => {
  tabulator.value = new Tabulator(table.value, {
    data: props.data,
    reactiveData: true,
    autoColumns: true,
    layout: "fitDataStretch",
    columnDefaults: {
      maxWidth: 500,
    },
    pagination: true,
    paginationSize: 10,
    paginationCounter: (
      pageSize,
      currentRow,
      currentPage,
      totalRows,
      totalPages
    ) => {
      return `Showing ${currentRow}-${currentRow + pageSize} of ${
        props.data.length
      } rows`;
    },
  });
});
</script>

<style>
.tabulator .tabulator-footer .tabulator-page.active {
  color: rgba(0, 0, 0, 0.87);
}
.tabulator {
  margin-top: 0;
}
</style>
