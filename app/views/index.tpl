<!DOCTYPE html>
<html>
  <head>
<!-- ___________________________ Metatags __________________________ -->
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name=viewport content="width=device-width, initial-scale=1">
    <title>Курсы валют ЦБ РФ</title>
    <meta name="author" content="Rockdukan">
    <meta name="description" content="Проект на фреймворке Bottle. Курсы валют ЦБ РФ.">
    <!-- https://www.flaticon.com/ru/free-icons/ -->
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png">

<!-- _____________________________ CSS _____________________________ -->
    <link rel="stylesheet" href="/static/css/style.css">

<!-- ______________________ If Internet Explorer ___________________ -->
    <script>
        if (/Trident\/|MSIE/.test(window.navigator.userAgent)) {
            alert("Ваш браузер не поддерживается!!!");
        }
    </script>
  </head>
  <body>
<!-- ______________________________ CONTENT ________________________ -->
    <div class="container">
      <h1>Курс валют ЦБ РФ</h1>
      <form method="get">
        <div class="form-controls">
          <fieldset>
            <legend>Выберите валюты:</legend>
            <div class="currency-options">
              <!-- Чекбоксы для выбора валют -->
              % for code, name in currencies.items():
                <label>
                  <input type="checkbox" name="currencies" value="{{code}}" {{'checked' if code in selected else ''}}>
                  {{name}}
                </label>
              % end
            </div>
          </fieldset>
          <!-- Поля для выбора дат -->
          <div class="date-range">
            <label>С:
              <input type="date" name="from_date" value="{{from_date}}">
            </label>
            <label>По:
              <input type="date" name="to_date" value="{{to_date}}">
            </label>
            <button type="submit">Показать</button>
          </div>
        </div>
      </form>
      <div class="chart-container">
        <canvas id="currencyChart"></canvas>
      </div>
    </div>
<!-- ____________________________ END_CONTENT ______________________ -->

<!-- ____________________________ JavaScript _______________________ -->
    <script src="/static/js/chart.js"></script>
    <script>
      const labels = {{!labels}};
      const data = {{!data}};
      const currencyNames = {{!currencies}};
      const colorPalette = [
        '#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FFCD56', '#4BC0C0', '#C9CBCF', '#7B68EE',
        '#3CB371', '#DC143C', '#FF69B4', '#00CED1', '#FFD700',
        '#00FA9A', '#8A2BE2', '#FF4500', '#2E8B57', '#ADFF2F'
      ];

      const datasets = Object.entries(data).map(([code, values], index) => {
        const color = colorPalette[index % colorPalette.length];
        return {
          label: currencyNames[code] || code,
          data: values,
          fill: false,
          borderColor: color,
          tension: 0.1
        };
      });

      new Chart(document.getElementById('currencyChart'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top'
            },
            title: {
              display: true,
              text: 'Динамика курса валют (ЦБ РФ)'
            }
          }
        }
      });
    </script>
  </body>
</html>
