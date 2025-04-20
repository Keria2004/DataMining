const rawData = document.getElementById("ingredient-data").dataset.ingredients;
const ingredientsList = JSON.parse(rawData);

// Dropdown logic
function showDropdown() {
  document.getElementById("dropdownList").style.display = 'block';
}

function selectIngredient(ingredient) {
  const inputField = document.getElementById("ingredientInput");
  let parts = inputField.value.split(',');
  parts[parts.length - 1] = ' ' + ingredient;
  inputField.value = parts.join(',').replace(/^,/, '').trim() + ', ';
  document.getElementById("dropdownList").style.display = 'none';
}

function filterIngredients() {
  const searchValue = document.getElementById("ingredientInput").value.toLowerCase().split(',').pop().trim();
  const dropdown = document.getElementById("dropdownList");
  dropdown.innerHTML = '';

  if (searchValue.length > 0) {
    ingredientsList.forEach(ingredient => {
      if (ingredient.toLowerCase().startsWith(searchValue)) {
        const div = document.createElement('div');
        div.textContent = ingredient;
        div.onclick = () => selectIngredient(ingredient);
        dropdown.appendChild(div);
      }
    });
    dropdown.style.display = dropdown.children.length > 0 ? 'block' : 'none';
  } else {
    dropdown.style.display = 'none';
  }
}

window.addEventListener('click', function (event) {
  if (!event.target.closest('.dropdown-container')) {
    document.getElementById("dropdownList").style.display = 'none';
  }
});

// Tag suggestion logic
const tagContainer = document.getElementById('tagList');
const previewTags = ingredientsList.slice(0, 20);
const hiddenTags = ingredientsList.slice(20);

previewTags.forEach(ingredient => {
  createTag(ingredient);
});

if (hiddenTags.length > 0) {
  const moreTag = document.createElement('div');
  moreTag.className = 'tag';
  moreTag.textContent = `+${hiddenTags.length} more`;
  moreTag.style.fontWeight = 'bold';
  moreTag.onclick = () => {
    hiddenTags.forEach(ingredient => createTag(ingredient));
    moreTag.remove();
  };
  tagContainer.appendChild(moreTag);
}

function createTag(ingredient) {
  const tag = document.createElement('div');
  tag.className = 'tag';
  tag.textContent = ingredient;

  tag.onclick = () => {
    const inputField = document.getElementById("ingredientInput");
    let parts = inputField.value.trim().split(/\s+/).filter(p => p);

    if (tag.classList.contains('selected')) {
      // GỠ chọn → xoá khỏi input
      tag.classList.remove('selected');
      parts = parts.filter(item => item.toLowerCase() !== ingredient.toLowerCase());
    } else {
      // CHỌN → thêm nếu chưa có
      if (!parts.includes(ingredient)) {
        parts.push(ingredient);
      }
      tag.classList.add('selected');
    }

    inputField.value = parts.join(' ');
  };

  tagContainer.appendChild(tag);
}


function addIngredientToInput(ingredient) {
  const inputField = document.getElementById("ingredientInput");
  let parts = inputField.value.trim().split(/\s+/); 

  if (!parts.includes(ingredient)) {
    parts.push(ingredient);
  }

  inputField.value = parts.join(' ');
}
