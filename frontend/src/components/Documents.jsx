import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useState } from "react";
import api from "../api/axios";
useEffect;
function Documents() {
  const [documents, setDocuments] = useState([]);
  useEffect(() => {
    api.get("/documents/").then(({ data }) => {
      console.log(data);

      setDocuments(data);
    });
  }, []);

  const columns = [
    { field: "id", headerName: "id", width: 90 },
    { field: "title", headerName: "title", width: 300 },
    { field: "created_at", headerName: "created_at", width: 200 },
  ];
  return (
    <>
      <DataGrid rows={documents} columns={columns} pageSize={10} />
    </>
  );
}

export default Documents;
