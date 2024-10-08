let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions= {

    columnDefs:[
        { className: "centrar", targets: [0,1,2,3,4,5]},
        { orderable:false, targets:[0,1,2,3,4,5]},
    ],

    pageLength: 4,
    destroy: true,

    language: {
        lengthMenu: "Mostrar _MENU_ registros por página",
        zeroRecords: "Ningún usuario encontrado",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ registros",
        infoEmpty: "Ningún usuario encontrado",
        infoFiltered: "(filtrados desde _MAX_ registros totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listUsers();

    dataTable = $("#datatable_user").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listUsers=async() => {
    try {
        const response = await fetch("https://jsonplaceholder.typicode.com/users");
        const users = await response.json();
        
        let content = ``;
        users.forEach((user,index)=>{
            content+=`
            <tr>
                <td>${index+1}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td>${user.address.city}</td>
                <td><i class="fa-solid fa-pencil"></i></td>
                <td><button class="btn btn-sm btn-primary"><i class="fa-solid fa-pencil"></i></button>
                    <button class="btn btn-sm btn-danger"><i class="fa-solid fa-trash-can"></i></button>
                </td>
            </tr>`;
        });
        tableBody_users.innerHTML = content;
    }catch(ex){
        alert(ex);
    }
};

window.addEventListener("load", async() => {
    await initDataTable();
});

