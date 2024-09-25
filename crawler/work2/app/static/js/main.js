document.getElementById("book_form").addEventListener("submit", async (e) => {
  e.preventDefault();
  // 使用正确的ID获取书籍ID
  const b_id = document.getElementById("b_id_0").value;
  const res = await fetch(`/book/${b_id}/info`);
  const data = await res.json();
  const book_info = document.querySelector(".book_info");
  const book_details = document.querySelector(".book_details");
  book_info.innerHTML = `<img src="${data.b_cover}" alt="${data.b_name}" />`;
  book_details.innerHTML = `
  <h2>${data.b_name}</h2>
  <p>作者：${data.b_author}</p>
  <p>状态：${data.b_status}</p>
  <p>更新时间：${data.b_utime}</p>
  <p>章节数量：${data.b_cnum}</p>
  <p>简介：${data.b_intro}</p>`;
});

document
  .getElementById("chapter_form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const b_id = document.getElementById("b_id_1").value;
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;
    const res = await fetch(`/book/${b_id}/chapter/${start}/${end}`);
    const data = await res.json();
    const book_chapter_list = document.querySelector(".book_chapter_list");
    book_chapter_list.innerHTML = data
      .map(
        (chapter) => `<li>
        <a href="/static/book/${b_id}/chapter/${chapter.c_id}.txt" target="_blank">${chapter.c_name}</a></li>`
      )
      .join("");
  });
