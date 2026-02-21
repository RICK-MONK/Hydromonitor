<template>
  <v-container fluid bg-color="surface" class="live-page">
    <v-row class="mx-auto live-wrap" align="stretch">
      <!-- LEFT: BOTH charts, SAME width -->
      <v-col cols="12" md="9" class="charts-col">
        <figure class="highcharts-figure">
          <div id="tempChart" class="chart-box"></div>
        </figure>
        <figure class="highcharts-figure mt-4">
          <div id="humidityChart" class="chart-box"></div>
        </figure>
      </v-col>

      <!-- RIGHT: cards -->
      <v-col cols="12" md="3" class="cards-col">
        <v-card class="mb-5 analysis-card">
          <v-card-subtitle>Temperature</v-card-subtitle>
          <v-card-item>
            <span class="text-h3">{{ temperature }}</span>
          </v-card-item>
        </v-card>

        <v-card class="mb-5 analysis-card">
          <v-card-subtitle>Heat Index (Feels like)</v-card-subtitle>
          <v-card-item>
            <span class="text-h3">{{ heatindex }}</span>
          </v-card-item>
        </v-card>

        <v-card class="mb-5 analysis-card">
          <v-card-subtitle>Humidity</v-card-subtitle>
          <v-card-item>
            <span class="text-h3">{{ humidity }}</span>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from "vue";
import Highcharts from "highcharts";
import Exporting from "highcharts/modules/exporting";
import more from "highcharts/highcharts-more";
import { useMqttStore } from "@/store/mqttStore";

Exporting(Highcharts);
more(Highcharts);

defineOptions({ name: "LiveView" });

const Mqtt = useMqttStore();

const tempHiChart = ref(null);
const humidChart = ref(null);
const points = ref(10);
const shift = ref(false);

const reflowCharts = () => {
  tempHiChart.value?.reflow();
  humidChart.value?.reflow();
};

const createCharts = () => {
  tempHiChart.value = Highcharts.chart("tempChart", {
    chart: { zoomType: "x", height: 320, backgroundColor: "#000000" },
    title: { text: "Temperature and Heat Index Analysis", align: "left", style: { color: "#FFFFFF" } },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#FFFFFF" } },
      labels: { style: { color: "#FFFFFF" } },
    },
    yAxis: {
      title: { text: "Temperature / Heat Index", style: { color: "#FFFFFF" } },
      labels: { format: "{value} °C", style: { color: "#FFFFFF" } },
    },
    tooltip: { shared: true },
    legend: { itemStyle: { color: "#FFFFFF" } },
    series: [
      { name: "Temperature", type: "spline", data: [], turboThreshold: 0 },
      { name: "Heat Index", type: "spline", data: [], turboThreshold: 0 },
    ],
    credits: { enabled: false },
  });

  humidChart.value = Highcharts.chart("humidityChart", {
    chart: { zoomType: "x", height: 320, backgroundColor: "#000000" },
    title: { text: "Humidity Analysis", align: "left", style: { color: "#FFFFFF" } },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#FFFFFF" } },
      labels: { style: { color: "#FFFFFF" } },
    },
    yAxis: {
      title: { text: "Humidity", style: { color: "#FFFFFF" } },
      labels: { format: "{value} %", style: { color: "#FFFFFF" } },
    },
    tooltip: { shared: true },
    legend: { itemStyle: { color: "#FFFFFF" } },
    series: [{ name: "Humidity", type: "spline", data: [], turboThreshold: 0 }],
    credits: { enabled: false },
  });
};

watch(
  () => Mqtt.payload,
  (data) => {
    if (!data || !tempHiChart.value || !humidChart.value) return;
    if (
      typeof data.timestamp === "undefined" ||
      typeof data.temperature === "undefined" ||
      typeof data.heatindex === "undefined" ||
      typeof data.humidity === "undefined"
    ) {
      return;
    }

    if (points.value > 0) {
      points.value--;
    } else {
      shift.value = true;
    }

    tempHiChart.value.series[0].addPoint(
      { y: parseFloat(data.temperature.toFixed(2)), x: data.timestamp * 1000 },
      true,
      shift.value
    );
    tempHiChart.value.series[1].addPoint(
      { y: parseFloat(data.heatindex.toFixed(2)), x: data.timestamp * 1000 },
      true,
      shift.value
    );
    humidChart.value.series[0].addPoint(
      { y: parseFloat(data.humidity.toFixed(2)), x: data.timestamp * 1000 },
      true,
      shift.value
    );
  },
  { deep: true }
);

const temperature = computed(() => {
  if (Mqtt.payload && typeof Mqtt.payload.temperature !== "undefined") {
    return `${Mqtt.payload.temperature.toFixed(2)} °C`;
  }
  return "--";
});

const heatindex = computed(() => {
  if (Mqtt.payload && typeof Mqtt.payload.heatindex !== "undefined") {
    return `${Mqtt.payload.heatindex.toFixed(2)} °C`;
  }
  return "--";
});

const humidity = computed(() => {
  if (Mqtt.payload && typeof Mqtt.payload.humidity !== "undefined") {
    return `${Mqtt.payload.humidity.toFixed(2)} %`;
  }
  return "--";
});

onMounted(async () => {
  createCharts();
  await nextTick();
  requestAnimationFrame(() => reflowCharts());
  window.addEventListener("resize", reflowCharts);
  Mqtt.connect();
  setTimeout(() => {
    Mqtt.subscribe("620169874");
    Mqtt.subscribe("/elet2415");
  }, 3000);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", reflowCharts);
});
</script>

<style scoped>
.live-wrap {
  max-width: 1200px;
  width: 100%;
  padding: 4px;
}

.charts-col {
  min-width: 0;
}

.chart-box {
  width: 100%;
  min-height: 320px;
}

.highcharts-figure {
  border: 2px solid black;
  background-color: black;
  margin: 0;
}

.analysis-card {
  background-color: #000000 !important;
  color: #ffffff !important;
}

.analysis-card :deep(.v-card-subtitle),
.analysis-card :deep(.text-h3) {
  color: #ffffff !important;
}
</style>
