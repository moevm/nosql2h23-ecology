<template>
  <div class="container">
    <h4 class="text-center mt-3">MSE 12 Ecology</h4>
    <h5 class="text-center">
      Сервис обработки спутниковых карт и поиска аномалий
    </h5>

    <div id="accordion" class="accordion mt-2">
      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#loading"
          >
            Загрузка
          </button>
        </h2>
        <div id="loading" class="accordion-collapse collapse">
          <div class="accordion-body">
            Загрузить карты можно в разделе
            <span class="text-primary">Загрузить</span>
            , выберите нужные файлы, в предложенных полях введите желаемое имя
            для карт (может быть удобно для их поиска в системе)
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#queue"
          >
            Очередь обработки
          </button>
        </h2>
        <div id="queue" class="accordion-collapse collapse">
          <div class="accordion-body">
            Текущую очередь обработки можно отслеживать в разделе
            <span class="text-primary">Очередь</span>
            . Данная очередь содержит текущие обрабатываемые карты, и карты
            которые ещё не начали обрабатываться, но были загружены. Данная
            очередь не отражает прогресс нарезки карт для их отображения.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#maps"
          >
            Загруженные карты
          </button>
        </h2>
        <div id="maps" class="accordion-collapse collapse">
          <div class="accordion-body">
            В разделе
            <span class="text-primary">Карты</span>
            находятся все загруженные в систему карты, в том числе пока не
            обработанные и/или не нарезанные (они помечены соответствующими
            флажками). Там же можно открыть карту или её отчёт.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#map-view"
          >
            Просмотр карты
          </button>
        </h2>
        <div id="map-view" class="accordion-collapse collapse">
          <div class="accordion-body">
            В режиме просмотра карты можно выбирать слои для отображения: слой
            изображения самого снимка, и слой найденных объектов. Данные слои
            накладываются поверх стандартной карты OpenStreetMap.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#reports"
          >
            Отчёты
          </button>
        </h2>
        <div id="reports" class="accordion-collapse collapse">
          <div class="accordion-body">
            В разделе
            <span class="text-primary">Отчёты</span>
            находятся список отчётов уже обработанных карт, на которых найдены
            аномалии. Здесь можно открыть карту изображения, к которому
            относится отчет или перейти в просмотр самого отчёта по аномалиям
            найденным на изображении.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#reports-view"
          >
            Просмотр отчёта
          </button>
        </h2>
        <div id="reports-view" class="accordion-collapse collapse">
          <div class="accordion-body">
            В просмотре отчёта отображаются данные по всем найденным на
            изображении аномалиям. Там же можно открыть на просмотр одну
            отдельную аномалию или отобразить её на карте.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#anomalies"
          >
            Аномалии
          </button>
        </h2>
        <div id="anomalies" class="accordion-collapse collapse">
          <div class="accordion-body">
            В разделе
            <span class="text-primary">Аномалии</span>
            находятся все найденные области аномалий на полностью обработанных
            изображениях. Там же можно открыть на просмотр одну отдельную
            аномалию.
          </div>
        </div>
      </div>

      <div class="accordion-item">
        <h2 class="accordion-header">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#anomaly"
          >
            Просмотр аномалии
          </button>
        </h2>
        <div id="anomaly" class="accordion-collapse collapse">
          <div class="accordion-body">
            В режиме просмотра аномалии можно посмотреть все параметры найденной
            аномалии, отметить её на карте с помощью клавиши "Показать на
            карте", а так же открыть отчет изображения, на котором была найдена
            аномалия.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss"></style>
