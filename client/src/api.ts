export function obsidize(
  input: string,
  targetFileName: string | null
): Promise<Response> {
  return fetch("http://localhost:5000/obsidize", {
    method: "POST",
    body: JSON.stringify({
      input,
      targetFileName,
    }),
  });
}
