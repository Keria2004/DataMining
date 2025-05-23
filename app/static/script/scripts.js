document.addEventListener("DOMContentLoaded", () => {
  // Lấy dữ liệu nguyên liệu từ data attribute
  const dataDiv = document.getElementById("ingredient-data");
  const raw = dataDiv?.dataset.ingredientList;
  let ingredientList = [];

  try {
    ingredientList = JSON.parse(raw).map(i => i.toLowerCase()).filter(Boolean);
    console.log("Ingredients loaded:", ingredientList.slice(0, 5));
  } catch (e) {
    console.error("Không thể đọc nguyên liệu từ data-ingredients", e);
  }

  const input = document.getElementById("ingredientInput");
  const suggestionBox = document.getElementById("suggestionList");

  // Xử lý input để hiện gợi ý nguyên liệu
  input.addEventListener("input", function () {
    const terms = this.value.trim().split(/\s+/);
    const lastWord = terms[terms.length - 1]?.toLowerCase() || "";
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

  // Ẩn suggestion khi click ngoài
  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !suggestionBox.contains(e.target)) {
      suggestionBox.innerHTML = "";
      suggestionBox.classList.add("hidden");
    }
  });

  // Cuộn xuống phần kết quả nếu có
  const resultSection = document.getElementById("resultSection");
  if (resultSection) {
    resultSection.scrollIntoView({ behavior: "smooth" });
  }

  // Xử lý nút xóa món yêu thích
  document.querySelectorAll('.btn-remove-favorite').forEach(btn => {
    btn.addEventListener('click', async function () {
      const recipeId = this.dataset.recipeId;
      if (!confirm('Bạn có chắc muốn xóa món này khỏi danh sách yêu thích?')) return;

      try {
        const response = await fetch(`/favorite/${recipeId}`, {
          method: 'POST',
          credentials: 'same-origin'
        });
        if (response.status === 204) {
          const card = this.closest('div');
          if (card) card.remove();
          showToast('Đã loại bỏ món ăn khỏi danh sách yêu thích.');
        } else {
          showToast('Lỗi khi xóa món ăn.');
        }
      } catch {
        showToast('Không thể kết nối đến server.');
      }
    });
  });
});

// Hàm hiện thông báo toast
function showToast(message) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('opacity-100', 'pointer-events-auto');
  toast.classList.remove('opacity-0', 'pointer-events-none');
  setTimeout(() => {
    toast.classList.remove('opacity-100', 'pointer-events-auto');
    toast.classList.add('opacity-0', 'pointer-events-none');
  }, 3000);
}

// Hàm toggle yêu thích món ăn
async function toggleFavorite(button) {
  const recipeId = button.getAttribute('data-recipe-id');
  try {
    const response = await fetch(`/favorite/${recipeId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      credentials: 'same-origin'
    });

    if (response.status === 204) {
      if (button.classList.contains('favorited')) {
        button.classList.remove('favorited');
        button.textContent = '❤️';
        showToast('Món ăn đã được bỏ khỏi mục yêu thích.');
      } else {
        button.classList.add('favorited');
        button.textContent = '💖';
        showToast('Món ăn đã được lưu vào mục yêu thích.');
      }
    } else if (response.status === 401) {
      showToast('Bạn cần đăng nhập để thêm món yêu thích.');
      window.location.href = '/login';
    } else {
      showToast('Đã xảy ra lỗi khi xử lý yêu thích. Vui lòng thử lại.');
    }
  } catch (error) {
    console.error('Lỗi khi toggle favorite:', error);
    showToast('Không thể kết nối đến server.');
  }
}
