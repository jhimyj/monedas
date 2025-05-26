export function saveUserToStorage(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

export function getUserFromStorage() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

export function removeUserFromStorage() {
  localStorage.removeItem("user");
}