/**
 * Добавляет новое поле ввода ингредиента, если не превышен лимит
 */
function addIngredient() {
    if (!adding_in_progress & (ingredient_index_global < INGREDIENTS_LIMIT)) {
        chooseGroup(ingredient_index_global);
    } else {
        alert(`Не могу добавить больше ${INGREDIENTS_LIMIT} ингредиентов`);
    }
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Настраивает меню ввода группы ингредиента для работы с полем ввода ингредиента
 * и выводит его на страницу.
 * @param {[Number]} ingredient_index индекс поля ввода
 */
function chooseGroup(ingredient_index) {
    var counter = 0;
    var group_button = document.getElementById(`group_button_${counter}`);
    while (group_button = document.getElementById(`group_button_${counter}`)) {
        group_button.setAttribute(
            'onclick',
            `changeGroup(${ingredient_index}, \'${group_button.getAttribute('data-index')}\');`
        );
        counter++;
    }
    groupMenuSwitch();
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Изменяет группу ингредиента коктейля.
 * @param {[Number]} ingredient_index индекс поля ввода
 * @param {[String]} group_index индекс (URL) группы ингредиента
 */
function changeGroup(ingredient_index, group_index) {
    var counter = 0;
    var group_name = "";
    var group_button = document.getElementById(`group_button_${counter}`);
    while (group_button) {
        if (group_button.getAttribute('data-index') == group_index) {
            group_name = group_button.getAttribute('data-name');
        }
        counter++;
        try {
            group_button = document.getElementById(`group_button_${counter}`);
        } catch {
            group_button = false;
        }
    }

    var selector_box = document.getElementById(`id_group_selector_box_${ingredient_index}`);
    var selector = document.getElementById(`group_selector_${ingredient_index}`);
    selector_box.removeChild(selector);

    selector = document.createElement('div');
    var selector_image = document.createElement('img');
    selector.id = `group_selector_${ingredient_index}`;
    selector.className = 'group__selector__box__info';
    if (group_index != '') {
        selector_image.src = `/static/images/ingredients/${group_index}.jpg`;
    } else {
        selector_image.src = `/static/images/ingredients/unknown.jpg`;
    }

    selector.appendChild(selector_image);
    selector.appendChild(document.createTextNode(group_name));
    selector_box.appendChild(selector);

    var group_input = document.getElementById(`id_ingredient_group_${ingredient_index}`);
    group_input.value = group_index;

    var input_box = document.getElementById(`id_recipe_item_input_box_${ingredient_index}`);
    input_box.style.display = 'flex';

    if (ingredient_index_global == ingredient_index) {
        ingredient_index_global++;
    }
    if (adding_in_progress) { groupMenuSwitch(); }
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Включает/выключает меню выбора группы ингредиента в зависимости от текущего статуса ввода.
 */
function groupMenuSwitch() {
    group_menu = document.getElementById('choose_group');
    if (adding_in_progress) {
        group_menu.style.opacity = 0;
        group_menu.style.pointerEvents = 'none';

    } else {
        group_menu.style.opacity = 1;
        group_menu.style.pointerEvents = 'auto';
    }
    adding_in_progress = !adding_in_progress;
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Включает/выключает меню выбора категории коктейля перед сохранением формы.
  * @param {[*]} event объект события
 */
function typeMenuSwitch(event) {
    type_menu = document.getElementById('choose_cocktail_type');
    if (save_in_progress) {
        type_menu.style.opacity = 0;
        type_menu.style.pointerEvents = 'none';
    } else {
        event.preventDefault();
        type_menu.style.opacity = 1;
        type_menu.style.pointerEvents = 'auto';
    }
    save_in_progress = !save_in_progress;
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Убирает поле ввода ингредиента со страницы (из видимой части).
 * Обнуляет введенные значения.
 * @param {[Number]} ingredient_index индекс поля ввода ингредиента
 */
function deleteIngredient(ingredient_index) {
    var answer = window.confirm("Удалить?");
    if (answer) {
        if (ingredient_index < ingredient_index_global) {
            var i = ingredient_index;
            while (i < ingredient_index_global) {
                i++;
                transferValues(i - 1, i);
            }
        }
        ingredient_index_global--;
        var input_box = document.getElementById(`id_recipe_item_input_box_${ingredient_index_global}`);
        input_box.removeAttribute('style');
    }
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Переносит значения из поля ввода ингредиентов формы source_index в target_index.
 * @param {[Number]} target_index индекс поля ввода назначения
 * @param {[Number]} source_index индекс поля ввода источника
 */
function transferValues(target_index, source_index) {
    var source_ingredient_input = document.getElementById(`id_ingredient_input_${source_index}`);
    var source_ingredient_value = document.getElementById(`id_ingredient_value_${source_index}`);
    var source_ingredient_unit = document.getElementById(`id_ingredient_unit_${source_index}`);
    var source_ingredient_group = document.getElementById(`id_ingredient_group_${source_index}`);

    var target_ingredient_input = document.getElementById(`id_ingredient_input_${target_index}`);
    var target_ingredient_value = document.getElementById(`id_ingredient_value_${target_index}`);
    var target_ingredient_unit = document.getElementById(`id_ingredient_unit_${target_index}`);

    changeGroup(target_index, source_ingredient_group.value);

    target_ingredient_input.value = source_ingredient_input.value;
    target_ingredient_value.value = source_ingredient_value.value;
    target_ingredient_unit.value = source_ingredient_unit.value;

    source_ingredient_input.value = '';
    source_ingredient_value.value = '';
    source_ingredient_unit.selectedIndex = 0;
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Проверяет поля с числом на соответствие целому положительному числу.
 * Если ввод не соответствует требованиям, изменяет поле ввода
 * @param {[Number]} ingredient_index индекс поля ввода количества ингредиента
 */
function checkIntInput(ingredient_index) {
    var input_box = document.getElementById(`id_ingredient_value_${ingredient_index}`);
    var input_str = input_box.value;
    input_str = input_str.replace(/[^0-9.,]/ig, "");
    input_str = input_str.replaceAll(",", ".");
    input_str = Math.abs(Math.round(input_str * 1));
    if (isNaN(input_str)) {
        input_box.value = "";
    } else {
        input_box.value = input_str;
    }
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Проверяет введенную строку на соответствие языковому паттерну.
 * Удаляет из поля ввода все символы, которые паттерну не соответствуют.
 * @param {[Number]} ingredient_index индекс поля ввода названия ингредиента
 * @param {[Number]} language код языкового паттерна
 */
function checkTextInput(ingredient_index, language) {
    var input_box = document.getElementById(INPUT_IDS[ingredient_index]);

    var input_str = input_box.value;
    input_str = input_str.replace(PATTERNS[language], '');
    input_str = input_str.replace(/^[ \t]+/gm, '');
    input_str = input_str.replace(/[ \t]+/g, ' ');

    input_str = input_str.charAt(0).toUpperCase() + input_str.slice(1);
    input_box.value = input_str;
}

/**
 * Предназначено для формы добавления рецепта коктейля.
 * Устанавливает тип коктейля и вызывает сохранение формы.
 * @param {[String]} cocktail_group тип коктейля
 */
function saveCocktail(cocktail_group) {
    var input_box = document.getElementById('id_cocktail_group');
    input_box.value = cocktail_group;
    document.forms[1].submit();
}

/**
 * Включает и выключает слайд-шоу на главной странице
 * @param {[String]} carousel_index индекс слайд-шоу
 */
function switchCarousel(carousel_index) {
    const carousels = document.getElementsByClassName('carousel__box');
    Array.prototype.forEach.call(carousels, node => {
        node.removeAttribute('style');
    });
    var node = document.getElementById(`id_carousel_box_${carousel_index}`);
    node.setAttribute('style', 'display: flex;');
}