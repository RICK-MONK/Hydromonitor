<template>
  <v-container fluid bg-color="surface">
    <v-row style="max-width: 1200px" class="mx-auto pa-1">
      <v-col cols="12" md="6">
        <v-sheet class="pa-2" height="250">
          <p>Enter date range for Analysis</p>
          <v-divider class="my-2" />
          <v-text-field
            v-model="start"
            label="Start date"
            type="date"
            density="compact"
            variant="solo-inverted"
            class="mr-5"
            style="max-width: 300px"
            flat
          />
          <v-text-field
            v-model="end"
            label="End date"
            type="date"
            density="compact"
            variant="solo-inverted"
            style="max-width: 300px"
            flat
          />
          <v-spacer />
          <v-btn
            class="text-caption mt-3"
            text="Analyze"
            color="primary"
            variant="tonal"
            @click="analyze"
          />
        </v-sheet>
      </v-col>

      <v-col cols="12" md="3" class="d-flex justify-center">
        <v-card
          title="Temperature"
          width="250"
          variant="outlined"
          color="primary"
          density="compact"
          rounded="lg"
        >
          <v-card-item class="mb-n5">
            <v-chip-group class="d-flex flex-row justify-center" color="primaryContainer" variant="flat">
              <v-tooltip text="Min" location="start">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ temperature.min }}</v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="Range" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ temperature.range }}</v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="Max" location="end">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ temperature.max }}</v-chip>
                </template>
              </v-tooltip>
            </v-chip-group>
          </v-card-item>

          <v-card-item align="center">
            <span class="text-h1 text-primary font-weight-bold">{{ temperature.avg }}</span>
          </v-card-item>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" class="d-flex justify-center">
        <v-card
          title="Humidity"
          width="250"
          variant="outlined"
          color="secondary"
          density="compact"
          rounded="lg"
        >
          <v-card-item class="mb-n5">
            <v-chip-group class="d-flex flex-row justify-center" color="secondaryContainer" variant="flat">
              <v-tooltip text="Min" location="start">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ humidity.min }}</v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="Range" location="top">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ humidity.range }}</v-chip>
                </template>
              </v-tooltip>
              <v-tooltip text="Max" location="end">
                <template #activator="{ props }">
                  <v-chip v-bind="props">{{ humidity.max }}</v-chip>
                </template>
              </v-tooltip>
            </v-chip-group>
          </v-card-item>

          <v-card-item align="center">
            <span class="text-h1 text-secondary font-weight-bold">{{ humidity.avg }}</span>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>

    <v-row style="max-width: 1200px" class="mx-auto">
      <v-col cols="12">
        <figure class="highcharts-figure">
          <div id="container"></div>
        </figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure">
          <div id="container0"></div>
        </figure>
      </v-col>
    </v-row>

    <v-row style="max-width: 1200px" class="mx-auto">
      <v-col cols="12" style="border: 1px solid black">
        <figure class="highcharts-figure">
          <div id="container1"></div>
        </figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure">
          <div id="container2"></div>
        </figure>
      </v-col>
      <v-col cols="12">
        <figure class="highcharts-figure">
          <div id="container3"></div>
        </figure>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
import { onMounted, reactive, ref } from "vue";
import { useAppStore } from "@/store/appStore";

Exporting(Highcharts);
more(Highcharts);

defineOptions({ name: "AnalysisView" });

const AppStore = useAppStore();

const start = ref("");
const end = ref("");

const temperature = reactive({ min: 0, max: 0, avg: 0, range: 0 });
const humidity = reactive({ min: 0, max: 0, avg: 0, range: 0 });

const tempHiChart = ref(null);
const humidChart = ref(null);
const histogramChart = ref(null);
const tempHiScatter = ref(null);
const humidHiScatter = ref(null);
const chartTextStyle = { color: "#FFFFFF" };

const createCharts = () => {
  tempHiChart.value = Highcharts.chart("container", {
    chart: { zoomType: "x", backgroundColor: "#000000" },
    title: { text: "Temperature and Heat Index Analysis", align: "left", style: chartTextStyle },
    subtitle: {
      text: 'The heat index, also known as the "apparent temperature," combines air temperature and relative humidity to estimate how hot it feels.',
      style: chartTextStyle,
    },
    xAxis: { type: "datetime", title: { text: "Time", style: chartTextStyle }, labels: { style: chartTextStyle } },
    yAxis: { title: { text: "Air Temperature & Heat Index", style: chartTextStyle }, labels: { format: "{value} deg C", style: chartTextStyle } },
    tooltip: { shared: true },
    legend: { itemStyle: chartTextStyle },
    series: [
      { name: "Temperature", type: "spline", data: [], turboThreshold: 0 },
      { name: "Heat Index", type: "spline", data: [], turboThreshold: 0 },
    ],
    credits: { enabled: false },
  });

  humidChart.value = Highcharts.chart("container0", {
    chart: { zoomType: "x", backgroundColor: "#000000" },
    title: { text: "Humidity Analysis", align: "left", style: chartTextStyle },
    xAxis: { type: "datetime", title: { text: "Time", style: chartTextStyle }, labels: { style: chartTextStyle } },
    yAxis: { title: { text: "Humidity", style: chartTextStyle }, labels: { format: "{value} %", style: chartTextStyle } },
    tooltip: { shared: true },
    legend: { itemStyle: chartTextStyle },
    series: [{ name: "Humidity", type: "spline", data: [], turboThreshold: 0 }],
    credits: { enabled: false },
  });

  histogramChart.value = Highcharts.chart("container1", {
    chart: { type: "column", zoomType: "x", backgroundColor: "#000000" },
    title: { text: "Frequency Distribution Analysis", align: "left", style: chartTextStyle },
    xAxis: { title: { text: "Bucket Start", style: chartTextStyle }, labels: { style: chartTextStyle } },
    yAxis: { title: { text: "Count", style: chartTextStyle }, labels: { style: chartTextStyle } },
    tooltip: { shared: true },
    legend: { itemStyle: chartTextStyle },
    series: [
      { name: "Temperature", type: "column", data: [], turboThreshold: 0 },
      { name: "Humidity", type: "column", data: [], turboThreshold: 0 },
      { name: "Heat Index", type: "column", data: [], turboThreshold: 0 },
    ],
    credits: { enabled: false },
  });

  tempHiScatter.value = Highcharts.chart("container2", {
    chart: { type: "scatter", zoomType: "x", backgroundColor: "#000000" },
    title: { text: "Temperature & Heat Index Correlation Analysis", align: "left", style: chartTextStyle },
    subtitle: {
      text: "Visualize the relationship between Temperature and Heat Index as well as patterns in the data",
      style: chartTextStyle,
    },
    xAxis: { title: { text: "Temperature", style: chartTextStyle }, labels: { format: "{value} deg C", style: chartTextStyle } },
    yAxis: { title: { text: "Heat Index", style: chartTextStyle }, labels: { format: "{value} deg C", style: chartTextStyle } },
    tooltip: { pointFormat: "Temperature: {point.x} deg C <br/> Heat Index: {point.y} deg C" },
    legend: { itemStyle: chartTextStyle },
    series: [{ name: "Analysis", data: [], turboThreshold: 0 }],
    credits: { enabled: false },
  });

  humidHiScatter.value = Highcharts.chart("container3", {
    chart: { type: "scatter", zoomType: "x", backgroundColor: "#000000" },
    title: { text: "Humidity & Heat Index Correlation Analysis", align: "left", style: chartTextStyle },
    subtitle: {
      text: "Visualize the relationship between Humidity and Heat Index as well as patterns in the data",
      style: chartTextStyle,
    },
    xAxis: { title: { text: "Humidity", style: chartTextStyle }, labels: { format: "{value} %", style: chartTextStyle } },
    yAxis: { title: { text: "Heat Index", style: chartTextStyle }, labels: { format: "{value} deg C", style: chartTextStyle } },
    tooltip: { pointFormat: "Humidity: {point.x} % <br/> Heat Index: {point.y} deg C" },
    legend: { itemStyle: chartTextStyle },
    series: [{ name: "Analysis", data: [], turboThreshold: 0 }],
    credits: { enabled: false },
  });
};

const updateCards = async (startDate, endDate) => {
  const temp = await AppStore.getTemperatureMMAR(startDate, endDate);
  const humid = await AppStore.getHumidityMMAR(startDate, endDate);

  if (temp?.length) {
    temperature.max = temp[0].max.toFixed(1);
    temperature.min = temp[0].min.toFixed(1);
    temperature.avg = temp[0].avg.toFixed(1);
    temperature.range = temp[0].range.toFixed(1);
  }

  if (humid?.length) {
    humidity.max = humid[0].max.toFixed(1);
    humidity.min = humid[0].min.toFixed(1);
    humidity.avg = humid[0].avg.toFixed(1);
    humidity.range = humid[0].range.toFixed(1);
  }
};

const updateLineCharts = async (startDate, endDate) => {
  const data = await AppStore.getAllInRange(startDate, endDate);

  const temperatureSeries = [];
  const heatindexSeries = [];
  const humiditySeries = [];

  data.forEach((row) => {
    temperatureSeries.push({ x: row.timestamp * 1000, y: parseFloat(row.temperature.toFixed(2)) });
    heatindexSeries.push({ x: row.timestamp * 1000, y: parseFloat(row.heatindex.toFixed(2)) });
    humiditySeries.push({ x: row.timestamp * 1000, y: parseFloat(row.humidity.toFixed(2)) });
  });

  tempHiChart.value.series[0].setData(temperatureSeries);
  tempHiChart.value.series[1].setData(heatindexSeries);
  humidChart.value.series[0].setData(humiditySeries);

  const tempHiPoints = data.map((r) => [parseFloat(r.temperature.toFixed(2)), parseFloat(r.heatindex.toFixed(2))]);
  const humidHiPoints = data.map((r) => [parseFloat(r.humidity.toFixed(2)), parseFloat(r.heatindex.toFixed(2))]);

  tempHiScatter.value.series[0].setData(tempHiPoints);
  humidHiScatter.value.series[0].setData(humidHiPoints);
};

const updateHistogramCharts = async (startDate, endDate) => {
  const temp = await AppStore.getFreqDistro("temperature", startDate, endDate);
  const humid = await AppStore.getFreqDistro("humidity", startDate, endDate);
  const hi = await AppStore.getFreqDistro("heatindex", startDate, endDate);

  const t = [];
  const h = [];
  const hiArr = [];

  temp.forEach((row) => t.push({ x: row._id, y: row.count }));
  humid.forEach((row) => h.push({ x: row._id, y: row.count }));
  hi.forEach((row) => hiArr.push({ x: row._id, y: row.count }));

  histogramChart.value.series[0].setData(t);
  histogramChart.value.series[1].setData(h);
  histogramChart.value.series[2].setData(hiArr);
};

const analyze = async () => {
  if (!start.value || !end.value) return;

  const startDate = new Date(start.value).getTime() / 1000;
  const endDate = new Date(end.value).getTime() / 1000;

  await updateLineCharts(startDate, endDate);
  await updateCards(startDate, endDate);
  await updateHistogramCharts(startDate, endDate);
};

onMounted(() => {
  createCharts();
});
</script>

<style scoped>
figure {
  border: 2px solid black;
  background-color: #000000 !important;
}
</style>

