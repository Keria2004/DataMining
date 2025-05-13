document.addEventListener("DOMContentLoaded", () => {
  const dataDiv = document.getElementById("ingredient-data");
  const raw = dataDiv?.dataset.ingredients;
  let ingredientList = [];

  try {
    ingredientList = JSON.parse(raw).map(i => i.toLowerCase());
    console.log("Ingredients loaded:", ingredientList.slice(0, 5));
  } catch (e) {
    console.error("Không thể đọc nguyên liệu từ data-ingredients", e);
  }

  const input = document.getElementById("ingredientInput");
  const suggestionBox = document.getElementById("suggestionList");

  input.addEventListener("input", function () {
    const terms = this.value.trim().split(/\s+/);
    const lastWord = terms[terms.length - 1].toLowerCase();
    suggestionBox.innerHTML = "";

    if (lastWord.length === 0) {
      suggestionBox.classList.add("hidden");
      return;
    }

    const filtered = ingredientList.filter(item => item.startsWith(lastWord)).slice(0, 8);

    if (filtered.length === 0) {
      suggestionBox.classList.add("hidden");
      return;
    }

    filtered.forEach(ing => {
      const li = document.createElement("li");
      li.className = "px-4 py-2 hover:bg-gray-100 cursor-pointer text-black font-semibold";
      li.textContent = ing;
      li.onclick = () => {
        terms[terms.length - 1] = ing;
        input.value = terms.join(" ") + " ";
        suggestionBox.innerHTML = "";
        suggestionBox.classList.add("hidden");
        input.focus();
      };
      suggestionBox.appendChild(li);
    });

    suggestionBox.classList.remove("hidden");
  });

  // Ẩn dropmenu nếu click ra ngoài
  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
      suggestionBox.innerHTML = "";
      suggestionBox.classList.add("hidden");
    }
  });

  // Cuộn tới phần kết quả (nếu có)
  const resultSection = document.getElementById("resultSection");
  if (resultSection) {
    resultSection.scrollIntoView({ behavior: "smooth" });
  }
});
