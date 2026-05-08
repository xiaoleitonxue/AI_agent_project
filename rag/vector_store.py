import os.path
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import embed_model
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=get_abs_path(chroma_conf["persist_directory"]),
            embedding_function=embed_model
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separator=chroma_conf["separator"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_documents(self):
        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False

            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_save: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            elif read_path.endswith(".txt"):
                return txt_loader(read_path)
            else:
                raise []

        allowed_file_path: list[str] = listdir_with_allowed_type(
            chroma_conf["data_path"],
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_file_path:
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"[load_documents]文件{path}已存在，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.info(f"[load_documents]文件{path}为空，跳过")
                    continue

                split_document: list[Document] = self.splitter.split_documents(documents)

                if not split_document:
                    logger.info(f"[load_documents]文件{path}已切分完毕，没有有效文本内容，跳过")
                    continue

                self.vector_store.add_documents(split_document)
                save_md5_hex(md5_hex)
                logger.info(f"[load_documents]文件{path}已添加到向量库")
            except Exception as e:
                logger.error(f"[load_documents]文件{path}处理出错，{str(e)}", exc_info=True)
                continue