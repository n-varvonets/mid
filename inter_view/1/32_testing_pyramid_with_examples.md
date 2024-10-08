
# Пирамида тестирования

**Пирамида тестирования** — это концепция, которая описывает подход к организации и распределению различных уровней автоматизированных тестов в проекте. Она включает три уровня тестов: модульные тесты, интеграционные тесты и end-to-end тесты. Уровни тестов распределены в форме пирамиды, где основание представляет собой множество модульных тестов, а верхушка — небольшое количество end-to-end тестов.

## Уровни пирамиды тестирования

1. **Модульные тесты (Unit tests)** — основание пирамиды.
   - Это тесты, которые проверяют отдельные функции или модули кода.
   - Такие тесты быстро выполняются и охватывают большую часть кода проекта.
   - **Пример**: Тестирование функции калькулятора, которая выполняет сложение двух чисел.
   
   ```python
   def add(a, b):
       return a + b

   def test_add():
       assert add(2, 3) == 5
       assert add(-1, 1) == 0
   ```
   
2. **Интеграционные тесты (Integration tests)** — средняя часть пирамиды.
   - Эти тесты проверяют взаимодействие между различными модулями системы. Например, как контроллеры в веб-приложении взаимодействуют с базой данных.
   - Интеграционные тесты более сложные, их выполнение занимает больше времени.
   - **Пример**: Тестирование взаимодействия между контроллером и базой данных.

   ```python
   def test_user_creation(db):
       user = create_user('test_user', 'password')
       assert db.get_user('test_user') is not None
   ```

3. **End-to-End тесты (E2E)** — верхушка пирамиды.
   - Это тесты, которые проверяют всю систему целиком, симулируя поведение пользователя. Они проверяют, как приложение работает в реальных условиях.
   - Такие тесты самые медленные, и их выполнение может быть сложным.
   - **Пример**: Тестирование сценария регистрации пользователя через интерфейс веб-приложения с использованием Selenium.

   ```python
   from selenium import webdriver

   def test_user_registration():
       browser = webdriver.Chrome()
       browser.get("https://example.com/register")
       browser.find_element_by_name("username").send_keys("test_user")
       browser.find_element_by_name("password").send_keys("password123")
       browser.find_element_by_name("submit").click()
       assert "Welcome, test_user!" in browser.page_source
       browser.quit()
   ```

## Почему это **пирамида**, а не треугольник?

Концепция названа **пирамида**, потому что основание (модульные тесты) должно быть самым широким и массивным. Чем выше уровень тестов (интеграционные и E2E), тем их должно быть меньше. Это обеспечивает правильный баланс между производительностью тестов и их покрытием.

Если модель тестирования перекошена, например, много End-to-End тестов и мало модульных, то это создаёт **неэффективную "перевёрнутую пирамиду"**, которая приводит к замедлению тестирования, частым ошибкам и трудностям в поддержке тестов.

### Пример неправильного баланса тестов:

Если у вас много E2E тестов и мало модульных:

1. Модульные тесты: 10 тестов.
2. Интеграционные тесты: 20 тестов.
3. End-to-End тесты: 100 тестов.

Это создаёт обратную пирамиду (или треугольник), что замедляет разработку и приводит к более хрупкому тестированию.

### Пример правильного баланса:

1. Модульные тесты: 100 тестов. (отдельные функции без зависимости от внешних систем или Мок тестирование(изолировать тестируемую функцию от внешних зависимостей) или фейк(отдельній класс которій иметриует работу бд, как ОРМ, напрмиер))
2. Интеграционные тесты: 20 тестов. (взаимодействие с бд и внешними апи)
3. End-to-End тесты: 10 тестов. (прохождение юезр кейсов)


Этот баланс обеспечивает эффективное покрытие, быструю обратную связь и простоту поддержки тестов.


