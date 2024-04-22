import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoModel, AutoConfig

class TipsyModel(nn.Module):
    "Tipsy无监督模型定义"

    def __init__(self, pretrained_model, pooling, dropout=0.3):
        super(TipsyModel, self).__init__()
        config = AutoConfig.from_pretrained(pretrained_model)
        config.attention_probs_dropout_prob = dropout
        self.bert = AutoModel.from_pretrained(pretrained_model, config=config)
        self.pooling = pooling
    
    def forward(self, input_ids, attention_mask, token_type_ids):
        out = self.bert(input_ids, attention_mask, token_type_ids)
        if self.pooling == 'cls':
            return out.last_hidden_state[:,0]
        if self.pooling == 'pooler':
            return out.pooler_output
        if self.pooling == 'last-avg':
            last = out.last_hidden_state.transpose(1, 2)
            return torch.avg_pool1d(last, kernel_size=last.shape[-1]).squeeze(-1)
        if self.pooling == 'first-last-avg':
            first = out.hidden_state[1].transpose(1, 2)
            last = out.hidden_state[-1].transpose(1, 2)
            first_avg = torch.avg_pool1d(first, kernel_size=first.shape[-1]).squeeze(-1)
            last_avg = torch.avg_pool1d(last, kernel_size=last.shape[-1]).squeeze(-1)
            avg = torch.cat(first_avg, last_avg, dim=1)
            return torch.avg_pool1d(avg, kernel_size=2).squeeze(-1)
    

def tipsy_unsup_loss(y_pred, device, temp=0.05):
    """
    无监督损失
    y_pred, Bert输出, [batch_size*2, 768]
    """
    y_true = torch.arange(y_pred.shape[0], device=device)
    y_true = (y_true - y_true%2*2)+1
    sim = F.cosine_similarity(y_pred.unsqueeze(1), y_pred.unsqueeze(0), dim=-1)
    sim = sim - torch.eye(y_pred.shape[0], device=device)*1e12
    sim = sim/temp
    loss = F.cross_entropy(sim, y_true)
    return torch.mean(loss)
