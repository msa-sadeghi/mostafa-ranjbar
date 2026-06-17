import { Box, Button, Container, TextField } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
function Login() {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/token/", credentials);
      localStorage.setItem("token", data.access);
      navigate("/dashboard");
    } catch (e) {
      console.log(e);
    }
  };
  return (
    <Container maxWidth="sm">
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 8 }}>
        <TextField
          fullWidth
          margin="normal"
          type="text"
          value={credentials.username}
          onChange={(e) =>
            setCredentials({ ...credentials, username: e.target.value })
          }
        />
        <TextField
          variant="outlined"
          fullWidth
          margin="normal"
          type="password"
          value={credentials.password}
          onChange={(e) =>
            setCredentials({ ...credentials, password: e.target.value })
          }
        />
        <Button type="submit" fullWidth variant="contained" sx={{ mt: 2 }}>
          login
        </Button>
      </Box>
    </Container>
  );
}

export default Login;
