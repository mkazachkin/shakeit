/**
 * Асинхронно получает JSON из API
 * @param {[String]} url адрес API
 * @returns {[Promise]} JSON полученный по API
 */
async function getJSON(url) {
    try {
        await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка при GET-запросе: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        throw new Error(`Ошибка при GET-запросе: ${error}`);
    }
}

/**
 * Меняет состояние лайка у рецепта, отправляя соответствующий запрос в API
 * @returns true в случае успеха, false, если лайк поставить не удалось
 */
async function sendLike() {
    const form = document.getElementById('id_likes_form');
    const url = form.getAttribute('action');
    const form_data = new FormData(form);
    const json_data = JSON.stringify(
        Object.fromEntries(
            form_data.entries()
        )
    );
    const csrf_token = getCookie('csrftoken');

    try {
        var result = await fetch(url, {
            method: "POST",
            headers: {
                "Content-type": "application/json;charset=UTF-8;",
                "X-CSRFToken": csrf_token,
            },
            body: json_data,
        });
        if (!result.ok) {
            console.error(`Ошибка при POST-запросе: ${error}`);
        }
        return result.ok;
    } catch (error) {
        console.error(`Ошибка при POST-запросе: ${error}`);
        return false;
    }
}

/**
 * Возвращает значение сохраненной Cookie
 * Функция взята со страницы
 * https://sky.pro/wiki/javascript/izvlechenie-znacheniy-iz-konkretnogo-cookie-v-java-script/
 * @param {[String]} name   имя cookie
 * @returns значение cooke
 */
function getCookie(name) {
    let cookie = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}


/**
 * Отрабатывает клик по символу лайка
 */
function likeClick() {
    const like_variable = document.getElementById('id_ll_is_like');
    var like = like_variable.value.toLowerCase();
    like = (like != 'true');
    like_variable.value = like;
    like_button = document.getElementById('id_like_button');
    dislike_button = document.getElementById('id_dislike_button');
    if (like) {
        like_button.setAttribute('style', 'display: none;');
        dislike_button.removeAttribute('style');
    } else {
        dislike_button.setAttribute('style', 'display: none;');
        like_button.removeAttribute('style');
    }
    sendLike();
}