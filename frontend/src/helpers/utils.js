export const isEmpty = value =>
  value === undefined ||
  value === null ||
  (typeof value === "object" && Object.keys(value).length === 0) ||
  (typeof value === "string" && value.trim().length === 0);

  export function isBottom(element) {
    if (element.scrollHeight - element.scrollTop === element.clientHeight) {
        return true;
    }
    else {
        return false;
    }
}